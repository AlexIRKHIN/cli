import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
import os
from collections import deque


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Инструмент визуализации графа зависимостей для менеджера пакетов',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--package',
        type=str,
        required=True,
        help='Имя анализируемого пакета в формате groupId:artifactId'
    )

    parser.add_argument(
        '--repo',
        type=str,
        required=True,
        help='URL-адрес репозитория или путь к файлу тестового репозитория'
    )

    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Режим работы с тестовым репозиторием'
    )

    parser.add_argument(
        '--version',
        type=str,
        required=True,
        help='Версия пакета'
    )

    parser.add_argument(
        '--max-depth',
        type=int,
        required=True,
        help='Максимальная глубина анализа зависимостей'
    )

    parser.add_argument(
        '--filter',
        type=str,
        default='',
        help='Подстрока для фильтрации пакетов'
    )

    return parser.parse_args()


def validate_arguments(args):
    """Проверка корректности аргументов"""
    errors = []

    if not args.package:
        errors.append("Имя пакета обязательно")
    elif ':' not in args.package and not args.test_mode:
        errors.append("Имя пакета должно быть в формате 'groupId:artifactId'")

    if not args.repo:
        errors.append("URL репозитория или путь к файлу обязателен")

    if not args.version:
        errors.append("Версия пакета обязательна")

    if args.max_depth <= 0:
        errors.append("Максимальная глубина должна быть положительным числом")

    return errors


def get_direct_dependencies(group, artifact, version, base_url):
    """
    Получает прямые зависимости Maven пакета из репозитория
    """
    try:
        # Формируем URL для POM файла
        path = f"{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}.pom"
        url = f"{base_url}/{path}"

        print(f"Загружаем POM из: {url}")

        # Загружаем POM файл
        with urllib.request.urlopen(url) as response:
            pom_content = response.read().decode('utf-8')

        # Парсим XML
        root = ET.fromstring(pom_content)

        # Находим все зависимости
        namespaces = {'maven': 'http://maven.apache.org/POM/4.0.0'}
        dependencies = []

        for dependency in root.findall('.//maven:dependency', namespaces):
            dep_group = dependency.find('maven:groupId', namespaces).text
            dep_artifact = dependency.find('maven:artifactId', namespaces).text
            dep_version_elem = dependency.find('maven:version', namespaces)
            dep_version = dep_version_elem.text if dep_version_elem is not None else "не указана"

            dependencies.append({
                'groupId': dep_group,
                'artifactId': dep_artifact,
                'version': dep_version
            })

        return dependencies

    except Exception as e:
        print(f"Ошибка при получении зависимостей: {e}")
        return []


def load_test_dependencies(file_path, package):
    """
    Загружает зависимости из тестового файла
    Формат файла: каждая строка - пакет и его зависимости через пробел
    """
    dependencies_map = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    dependencies_map[parts[0]] = parts[1:]
        return dependencies_map.get(package, [])
    except Exception as e:
        print(f"Ошибка при чтении тестового файла: {e}")
        return []


def build_dependency_graph(args):
    """
    Строит граф зависимостей с использованием DFS без рекурсии
    """
    print(f"\nПостроение графа зависимостей для: {args.package}")
    print(f"Максимальная глубина: {args.max_depth}")
    print(f"Фильтр: '{args.filter}'")

    graph = {}
    visited = set()
    stack = deque()

    # Добавляем корневой пакет в стек (пакет, глубина)
    stack.append((args.package, 0))

    while stack:
        current_package, depth = stack.pop()

        # Пропускаем если уже посещали или превышена глубина
        if current_package in visited or depth > args.max_depth:
            continue

        visited.add(current_package)

        # Применяем фильтр
        if args.filter and args.filter in current_package:
            print(f"Пропущен пакет (фильтр): {current_package}")
            continue

        # Получаем зависимости в зависимости от режима
        if args.test_mode:
            dependencies = load_test_dependencies(args.repo, current_package)
            # Преобразуем в формат для единообразия
            formatted_deps = [f"{dep}:1.0" for dep in dependencies]
        else:
            # Для реального режима парсим groupId:artifactId
            parts = current_package.split(':')
            if len(parts) != 2:
                print(f"Неверный формат пакета: {current_package}")
                continue
            group, artifact = parts
            deps = get_direct_dependencies(group, artifact, args.version, args.repo)
            formatted_deps = [f"{dep['groupId']}:{dep['artifactId']}" for dep in deps]

        graph[current_package] = formatted_deps

        # Добавляем зависимости в стек для дальнейшего обхода
        for dep in formatted_deps:
            if dep not in visited:
                # Проверяем циклические зависимости
                if any(dep in path for path, _ in stack):
                    print(f"Обнаружена циклическая зависимость: {dep}")
                else:
                    stack.append((dep, depth + 1))

    return graph


def analyze_package(args):
    """
    Основная функция анализа пакета
    """
    print(f"\nАнализ пакета: {args.package}")
    print(f"Версия: {args.version}")
    print(f"Репозиторий: {args.repo}")
    print(f"Тестовый режим: {args.test_mode}")

    # Строим граф зависимостей
    graph = build_dependency_graph(args)

    # Выводим результат
    print("\nГраф зависимостей:")
    for package, dependencies in graph.items():
        print(f"{package} -> {dependencies}")

    # Выводим статистику
    total_packages = len(graph)
    total_dependencies = sum(len(deps) for deps in graph.values())
    print(f"\nСтатистика:")
    print(f"Всего пакетов: {total_packages}")
    print(f"Всего зависимостей: {total_dependencies}")


def main():
    """Основная функция"""
    try:
        args = parse_arguments()

        # Проверка аргументов
        errors = validate_arguments(args)
        if errors:
            print("Ошибки проверки параметров:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

        # Вывод всех параметров (требование этапа 1)
        print("Параметры конфигурации:")
        print(f"  Пакет: {args.package}")
        print(f"  Репозиторий: {args.repo}")
        print(f"  Тестовый режим: {args.test_mode}")
        print(f"  Версия: {args.version}")
        print(f"  Максимальная глубина: {args.max_depth}")
        print(f"  Фильтр: {args.filter}")

        # Этап 2 и 3: Получение зависимостей и построение графа
        analyze_package(args)

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()