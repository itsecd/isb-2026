import argparse
import sys

import data_processing
import auth
import auth_no_salt
import collision


def get_args():
    """
    Парсинг командной строки
    """
    parser = argparse.ArgumentParser(description="Система аутентификации пользователя")
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-aut', '--authentication', action='store_true', help='Режим аутентификации с солью')
    mode_group.add_argument('-reg', '--registration', action='store_true', help='Режим регистрации с солью')
    mode_group.add_argument('-dec', '--decomposition', action='store_true', help='Режим подбора коллизии')
    mode_group.add_argument('-aut_nosalt', '--authentication_no_salt', action='store_true', help='Режим аутентификации без соли')
    mode_group.add_argument('-reg_nosalt', '--registration_no_salt', action='store_true', help='Режим регистрации без соли')

    parser.add_argument("--user", required=True, help="Имя пользователя")
    parser.add_argument("--password", required=True, help="Пароль")

    parser.add_argument("--path", help="Путь к логинам и паролям")
    parser.add_argument('--settings', type=str, default='settings.json', help='Путь к файлу конфигурации (по умолчанию settings.json)')

    return parser.parse_args()


def get_settings() -> dict:
    args = get_args()
    config = data_processing.load_json(args.settings)

    if args.authentication:
        mode = "aut"
    elif args.registration:
        mode = "reg"
    elif args.authentication_no_salt:
        mode = "aut_nosalt"
    elif args.registration_no_salt:
        mode = "reg_nosalt"
    else:
        mode = "dec"

    final_config = {
        "mode": mode,
        "user": args.user,
        "password": args.password,
        "path": args.path or config.get("path_to_data", "data")
    }
    return final_config


def main():
    """
    Основная функция программы с обработкой исключений
    """
    try:
        config = get_settings()
        data = data_processing.load_json(config["path"])

        match config["mode"]:
            case "aut":
                if auth.login_user(config["user"], config["password"], data):
                    print(f"Добро пожаловать, {config['user']}")
                else:
                    print("Ошибка в имени пользователя или в пароле")

            case "reg":
                if auth.register_user(config["user"], config["password"], data):
                    data_processing.save_json(config["path"], data)
                    print("Пользователь успешно зарегистрирован")
                else:
                    print(f"Пользователь {config['user']} уже существует")
                    
            case "dec":
                collision.run_collision_brute(config["user"], data)
                
            case "aut_nosalt":
                if auth_no_salt.login_user_no_salt(config["user"], config["password"], data):
                    print(f"Добро пожаловать, {config['user']}")
                else:
                    print("Ошибка в имени пользователя или в пароле")
                    
            case "reg_nosalt":
                if auth_no_salt.register_user_no_salt(config["user"], config["password"], data):
                    data_processing.save_json(config["path"], data)
                    print("Пользователь успешно зарегистрирован (БЕЗ СОЛИ)")
                else:
                    print(f"Пользователь {config['user']} уже существует")

    except Exception as e:
        print(f"Критическая ошибка выполнения: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()