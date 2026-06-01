import argparse
from backend import Auth
from app import run_gui

def main():
    """
    Главная точка входа в приложение.
    
    Поддерживает два режима работы:
        1. GUI режим (по умолчанию): Запускает графический интерфейс на PyQt5
        2. CLI режим: Демонстрирует брутфорс-атаку на простой хеш пароля "123"
        
    Аргументы командной строки:
        --mode {gui,cli}: Выбор режима запуска (по умолчанию: gui)
        
    Примеры использования:
        python main.py                # Запуск GUI
        python main.py --mode cli     # Запуск CLI демо брутфорса
        python main.py --mode gui     # Явный запуск GUI
        
    Примечание:
        В CLI режиме автоматически регистрируется пользователь "victim" с паролем "123",
        затем выполняется брутфорс-атака для демонстрации уязвимости SHA-256.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["gui", "cli"], default="gui")
    args = parser.parse_args()

    auth = Auth()

    if args.mode == "gui":
        run_gui(auth)
    else:
        # CLI режим: демонстрация брутфорс-атаки
        auth.unsafe_registration("victim", "123")
        row = auth.db.fetch_user("victim")
        print("HASH:", row[0])        # Вывод SHA-256 хеша пароля
        print("FOUND:", auth.bruteforce(row[0]))  # Взлом хеша перебором

    auth.close()

if __name__ == "__main__":
    main()