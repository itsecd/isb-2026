from file_open_and_close import *
from hash_comparison import *
from hash_generation import *
from picture_demonstration import *
from salt_generation import *
from user_login_and_registration import *
from no_crack import *
import argparse
import sys
from collision_finder import run_collision_attack
from gui_app import run_gui

def run_interactive_cli(path):
    while True:
        print("\n--- Password Storage and Checking (CLI) ---")
        print("1. User registration (Safe: Argon2id + Salt)")
        print("2. User login (Safe)")
        print("3. User registration (Unsafe: NO Salt)")
        print("4. User login (Unsafe)")
        print("5. Run Collision Attack Analysis (tqdm)")
        print("0. Exit")

        choice = input("Choose the scenario: ").strip()
    
        try:
            match choice:
                case "1":
                    user_registration(path)
                case "2":
                    if user_login(path):
                        vvod= input("Hey bud, wanna see some pussy? (Yes/No): ")
                    match vvod:
                        case "Yes":
                            show_picture(path)
                        case "No":
                            pass
                        case _:
                            print("Wrong choise, bud...")
                case "3":
                    user_registration_no_salt(path)
                case "4":
                    user_login_no_salt(path)
                case "5":
                    run_collision_attack(path)
                case "0":
                    print("Exit...")
                    break
                case _:  
                    print("Wrong mode, enter again.")
        except Exception as e:
            print(f"[EXCEPTION HANDLED]: An unexpected error occurred in CLI: {e}")

def main():
    path = 'settings.json'
    
    # Инициализация аргпарс
    parser = argparse.ArgumentParser(description="Cryptographic password storage system with vulnerability analysis.")
    parser.add_argument('--mode', choices=['cli', 'gui', 'crack'], default='cli',
                        help="Execution mode: interactive console (cli), PyQt graphical interface (gui), collision attack analysis (crack)")
    
    args = parser.parse_args()
    
    #Выбор режима (политического)
    try:
        if args.mode == 'gui':
            print("[+] Launching PyQt5 Graphical User Interface...")
            run_gui()
        elif args.mode == 'crack':
            run_collision_attack(path)
        else:
            run_interactive_cli(path)
    except Exception as e:
        print(f"[Critical Application Failure]: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEmergency exit activated. Goodbye!")