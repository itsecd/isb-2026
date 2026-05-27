import sys
import os
import json
import argparse
from hash_units import generate_salt, calculate_hash
from file_units import read_json_file, write_json_file, safe_load_database, DB_NOSALT, DB_SALT
from checks import check_login, check_secure_user_data, check_unsecure_user_data


def run_gui_mode() -> None:
    """
    Runs the program through the PyQt interface
    """

    from PyQt6.QtWidgets import QApplication
    from gui import AuthApp
    
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.exit(app.exec())


def run_console_mode(args: argparse.Namespace) -> None:
    """
    Launches the program via the console.

    Args:
        args (argparse.Namespace): Arguments entered by the user.
    """

    if not check_login(args.login):
        return

    match (args.mode, args.action):
        case ('sec', 'reg'):
            print(f"Mode: Secure Registration\n")

            database = safe_load_database(DB_SALT)
            if database is None:
                return

            if args.login in database:
                print(f"A user with that name already exists.")
                return

            salt = generate_salt()
            password_hash = calculate_hash(args.password, salt)  

            database[args.login] = {
                "hash": password_hash,
                "salt": salt
            }

            write_json_file(DB_SALT, database)
            print(f"Welcome to the secure club, {args.login}!")


        case ('unsec', 'reg'):
            print(f"Mode: Unsecure Registration\n")

            database = safe_load_database(DB_NOSALT)
            if database is None:
                return

            if args.login in database:
                print(f"A user with that name already exists.")
                return

            password_hash = calculate_hash(args.password)  

            database[args.login] = password_hash

            write_json_file(DB_NOSALT, database)
            print(f"Welcome to the unsecure club, {args.login}!")


        case ('sec', 'auth'):
            print(f"Mode: Secure Authorization\n")

            database = safe_load_database(DB_SALT)
            if database is None:
                return

            if len(database) == 0:
                print(f"There are no registered users in the system.\n"
                      f"Please register first.")
                return

            if args.login not in database:
                print(f"There is no such user in the database.\n"
                      f"Try to enter your username again or register.")
                return

            user_info = database[args.login]
            if not check_secure_user_data(user_info, args.login):
                return

            user_salt = user_info["salt"]
            old_password_hash = user_info["hash"]
            new_password_hash = calculate_hash(args.password, user_salt)

            if old_password_hash == new_password_hash:
                print(f"Welcome back to the secure club, {args.login}!")
            
            else:
                print(f"The password {args.password} is not suitable for the login {args.login}.\n"
                      f"Try to enter the password again.")


        case ('unsec', 'auth'):
            print(f"Mode: Unsecure Authorization\n")

            database = safe_load_database(DB_NOSALT)
            if database is None:
                return

            if len(database) == 0:
                print(f"There are no registered users in the system.\n"
                      f"Please register first.")
                return

            if args.login not in database:
                print(f"There is no such user in the database.\n"
                      f"Try to enter your username again or register.")
                return

            old_password_hash = database[args.login]
            if not check_unsecure_user_data(old_password_hash, args.login):
                return

            new_password_hash = calculate_hash(args.password)

            if old_password_hash == new_password_hash:
                print(f"Welcome back to the unsecure club, {args.login}!")
            
            else:
                print(f"The password {args.password} is not suitable for the login {args.login}.\n"
                      f"Try to enter the password again.")


def main():
    if '--cli' in sys.argv:
        parser = argparse.ArgumentParser(description="Hashing passwords and protecting credentials")
        parser.add_argument('--cli', action='store_true', help='run in console mode')

        group_mode = parser.add_mutually_exclusive_group(required = True)
        group_mode.add_argument('-sec', '--secured', action='store_const', const='sec', dest='mode', help='use secure storage mode (with salt)')
        group_mode.add_argument('-unsec', '--unsecured', action='store_const', const='unsec', dest='mode', help='use unsecure storage mode (without salt)')
        
        group_action = parser.add_mutually_exclusive_group(required = True)
        group_action.add_argument('-reg', '--registration', action='store_const', const='reg', dest='action', help='register a new user in the system')
        group_action.add_argument('-auth', '--authorization', action='store_const', const='auth', dest='action', help='authorize an existing user')
        
        parser.add_argument('-l', '--login', required=True, help='user identity login from 3 to 20 characters')
        parser.add_argument('-p', '--password', required=True, help='user password')
        
        args = parser.parse_args()
        run_console_mode(args)

    else:
        run_gui_mode()


if __name__ == "__main__":
    main()