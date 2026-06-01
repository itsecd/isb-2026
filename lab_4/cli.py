import argparse
import sys
from UserManager import UserManager, UserManagerError
import analysator

def run_cli():
    """
    Запускает CLI версию приложения
    CLI версия запускается, если имеется аргумент при запуске
    """
    parser = argparse.ArgumentParser(description="Система аутентификации и анализа безопасности")
    parser.add_argument("action", choices=["register", "auth", "crack"], help="Действие")
    parser.add_argument("-u", "--user", help="Логин пользователя")
    parser.add_argument("-p", "--password", help="Пароль пользователя")
    parser.add_argument("-a", "--algo", choices=["sha256", "sha256_salted", "bcrypt"], default="bcrypt", help="Алгоритм")

    args = parser.parse_args()
    manager = UserManager()

    try:
        if args.action == "register":
            if not args.user or not args.password:
                print("Ошибка: Для регистрации нужны -u и -p")
                return
            manager.register(args.user, args.password, args.algo)
            print(f"Пользователь {args.user} успешно зарегистрирован ({args.algo})!")
            
        elif args.action == "auth":
            if not args.user or not args.password:
                print("Ошибка: Для авторизации нужны -u и -p")
                return
            if manager.authenticate(args.user, args.password):
                print("Авторизация успешна! Добро пожаловать.")
            else:
                print("Ошибка: Неверный пароль.")
                
        elif args.action == "crack":
            analysator.vuln_analyse("qwerty")
            analysator.vuln_salt_analyse("qwerty")

    except UserManagerError as e:
        print(f"Ошибка бизнес-логики: {e}", file=sys.stderr)