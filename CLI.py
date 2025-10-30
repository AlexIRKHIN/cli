import argparse
import sys

# File

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
        help='Имя анализируемого пакета'
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

    if not args.repo:
        errors.append("URL репозитория или путь к файлу обязателен")

    if not args.version:
        errors.append("Версия пакета обязательна")

    if args.max_depth <= 0:
        errors.append("Максимальная глубина должна быть положительным числом")

    return errors


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

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()