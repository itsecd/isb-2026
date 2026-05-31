import argparse
import sys
import os

from modules.config import load_settings
from modules.auth import register_user, authenticate_user
from modules.hashing import (
    demonstrate_avalanche_effect,
    find_collision_simple
)


def create_parser() -> argparse.ArgumentParser:
    """
    Создаёт парсер аргументов командной строки.

    Returns:
        argparse.ArgumentParser: настроенный парсер.
    """
    parser = argparse.ArgumentParser(
        description='Система аутентификации. Лабораторная работа No4'
    )

    subparsers = parser.add_subparsers(dest='mode', help='Режим работы')

    reg_parser = subparsers.add_parser('register', help='Регистрация пользователя')
    reg_parser.add_argument('--username', '-u', required=True,
                           help='Логин пользователя')
    reg_parser.add_argument('--password', '-p', required=True,
                           help='Пароль пользователя')
    reg_parser.add_argument('--algorithm', '-a', choices=['sha256', 'bcrypt'],
                           default='sha256',
                           help='Алгоритм хеширования (по умолчанию sha256)')

    login_parser = subparsers.add_parser('login', help='Вход в систему')
    login_parser.add_argument('--username', '-u', required=True,
                             help='Логин пользователя')
    login_parser.add_argument('--password', '-p', required=True,
                             help='Пароль пользователя')

    subparsers.add_parser('avalanche', help='Демонстрация лавинного эффекта')

    collision_parser = subparsers.add_parser('collision',
                                            help='Поиск коллизии')
    collision_parser.add_argument('--bytes', '-b', type=int, default=2,
                                 help='Количество байт для сравнения (1-4)')

    subparsers.add_parser('gui', help='Запуск графического интерфейса')

    subparsers.add_parser('test', help='Запуск юнит-тестов')

    parser.add_argument('--settings', '-s', default='settings.json',
                       help='Путь к файлу настроек')

    return parser


def handle_register(args, settings: dict) -> None:
    """
    Обрабатывает режим регистрации пользователя.

    Args:
        args: аргументы командной строки.
        settings (dict): настройки приложения.
    """
    print("\nРегистрация пользователя\n")

    try:
        result = register_user(
            args.username,
            args.password,
            settings['users_file'],
            args.algorithm
        )

        if result['success']:
            print(f"Успех: {result['message']}")
            print(f"Алгоритм: {result['user_data']['algorithm']}")
            print(f"Хеш: {result['user_data']['hash'][:50]}...")
        else:
            print(f"Ошибка: {result['message']}")
            sys.exit(1)

    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


def handle_login(args, settings: dict) -> None:
    """
    Обрабатывает режим входа в систему.

    Args:
        args: аргументы командной строки.
        settings (dict): настройки приложения.
    """
    print("\nВход в систему\n")

    try:
        result = authenticate_user(
            args.username,
            args.password,
            settings['users_file']
        )

        if result['success']:
            print(f"Успех: {result['message']}")
        else:
            print(f"Ошибка: {result['message']}")
            sys.exit(1)

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


def handle_avalanche() -> None:
    """
    Обрабатывает режим демонстрации лавинного эффекта.
    """
    print("\nДемонстрация лавинного эффекта\n")
    demonstrate_avalanche_effect()


def handle_collision(args) -> None:
    """
    Обрабатывает режим поиска коллизии.

    Args:
        args: аргументы командной строки.
    """
    print(f"\nПоиск коллизии для {args.bytes} байт SHA-256\n")

    if args.bytes < 1 or args.bytes > 4:
        print("Ошибка: количество байт должно быть от 1 до 4.")
        sys.exit(1)

    result = find_collision_simple(args.bytes, show_progress=True)

    if result['message1'] is not None:
        print(f"\nКоллизия найдена!")
        print(f"Сообщение 1: {result['message1']}")
        print(f"Сообщение 2: {result['message2']}")
        print(f"Общий префикс хеша: {result['hash_prefix']}")
        print(f"Количество попыток: {result['attempts']}")
        print(f"Затраченное время: {result['time_seconds']:.2f} сек")
    else:
        print(f"\nКоллизия не найдена.")
        print(f"Количество попыток: {result['attempts']}")
        print(f"Затраченное время: {result['time_seconds']:.2f} сек")


def handle_gui(settings: dict) -> None:
    """
    Обрабатывает запуск графического интерфейса.

    Args:
        settings (dict): настройки приложения.
    """
    try:
        from modules.gui import run_gui
        run_gui(settings['users_file'],
               settings['default_hash_algorithm'])
    except ImportError as e:
        print(f"Ошибка: не удалось импортировать PyQt5: {e}")
        print("Установите PyQt5: pip install PyQt5")
        sys.exit(1)


def handle_test() -> None:
    """
    Обрабатывает запуск юнит-тестов.
    """
    import unittest

    print("\nЗапуск юнит-тестов\n")

    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\nВсе тесты пройдены успешно.")
    else:
        print(f"\nПровалено тестов: {len(result.failures)}")
        print(f"Ошибок: {len(result.errors)}")
        sys.exit(1)


def main() -> None:
    """
    Главная функция программы.

    Разбирает аргументы командной строки и запускает соответствующий режим.
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        sys.exit(1)

    settings = load_settings(args.settings)

    os.makedirs(os.path.dirname(settings['users_file']), exist_ok=True)

    match args.mode:
        case 'register':
            handle_register(args, settings)
        case 'login':
            handle_login(args, settings)
        case 'avalanche':
            handle_avalanche()
        case 'collision':
            handle_collision(args)
        case 'gui':
            handle_gui(settings)
        case 'test':
            handle_test()
        case _:
            parser.print_help()
            sys.exit(1)


if __name__ == '__main__':
    main()