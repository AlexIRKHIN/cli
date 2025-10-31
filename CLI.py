import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
import os


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
    elif ':' not in args.package:
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


def analyze_package(args):
    """
    Основная функция анализа пакета
    """
    print(f"\nАнализ пакета: {args.package}")
    print(f"Версия: {args.version}")
    print(f"Репозиторий: {args.repo}")

    # Парсим имя пакета (ожидаем формат groupId:artifactId)
    parts = args.package.split(':')
    if len(parts) != 2:
        print("Ошибка: имя пакета должно быть в формате 'groupId:artifactId'")
        return

    group, artifact = parts

    # Получаем зависимости
    dependencies = get_direct_dependencies(
        group, artifact, args.version, args.repo
    )

    # Выводим результат (требование этапа 2)
    if dependencies:
        print("\nПрямые зависимости пакета:")
        for i, dep in enumerate(dependencies, 1):
            print(f"{i}. {dep['groupId']}:{dep['artifactId']}:{dep['version']}")
    else:
        print("Прямые зависимости не найдены или произошла ошибка")


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
        # print("Параметры конфигурации:")
        # print(f"  Пакет: {args.package}")
        # print(f"  Репозиторий: {args.repo}")
        # print(f"  Тестовый режим: {args.test_mode}")
        # print(f"  Версия: {args.version}")
        # print(f"  Максимальная глубина: {args.max_depth}")
        # print(f"  Фильтр: {args.filter}")

        # Этап 2: Получение зависимостей
        analyze_package(args)

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()