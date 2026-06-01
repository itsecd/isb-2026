"""Консольный интерфейс системы аутентификации."""

import argparse
import json
from auth import register_user, authenticate_user


def load_config(path: str = "config.json") -> dict:
    """Загружает конфигурацию из JSON-файла.

    Args:
        path (str): Путь к файлу конфигурации.

    Returns:
        dict: Словарь с настройками.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """Точка входа консольного интерфейса."""
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Хеширование паролей и защита учетных данных"
    )

    group_mode = parser.add_mutually_exclusive_group(required=True)
    group_mode.add_argument(
        "-sec", "--secured",
        action="store_const", const="sec", dest="mode",
        help="Безопасный режим (с солью)"
    )
    group_mode.add_argument(
        "-unsec", "--unsecured",
        action="store_const", const="unsec", dest="mode",
        help="Небезопасный режим (без соли)"
    )

    group_action = parser.add_mutually_exclusive_group(required=True)
    group_action.add_argument(
        "-reg", "--registration",
        action="store_const", const="reg", dest="action",
        help="Регистрация нового пользователя"
    )
    group_action.add_argument(
        "-auth", "--authorization",
        action="store_const", const="auth", dest="action",
        help="Авторизация существующего пользователя"
    )

    parser.add_argument(
        "-l", "--login",
        required=True,
        help="Логин пользователя"
    )
    parser.add_argument(
        "-p", "--password",
        required=True,
        help="Пароль пользователя"
    )

    args = parser.parse_args()

    match (args.mode, args.action):
        case ("sec", "reg"):
            db_path = config["db_salt"]
            use_salt = True
            result = register_user(args.login, args.password, db_path, use_salt)
            print(result)

        case ("sec", "auth"):
            db_path = config["db_salt"]
            use_salt = True
            result = authenticate_user(args.login, args.password, db_path, use_salt)
            print(result)

        case ("unsec", "reg"):
            db_path = config["db_nosalt"]
            use_salt = False
            result = register_user(args.login, args.password, db_path, use_salt)
            print(result)

        case ("unsec", "auth"):
            db_path = config["db_nosalt"]
            use_salt = False
            result = authenticate_user(args.login, args.password, db_path, use_salt)
            print(result)


if __name__ == "__main__":
    main()