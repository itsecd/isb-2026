import argparse
import collisions
import gui
import utils

def parse_args() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки:
    -Выбор 1-го из 2-ух режимов работы программы на выбор
    -Путь до .json файла с настройками
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--cli", action="store_true", help="Запуск в режиме командной строки вместо GUI")
    group.add_argument("--gui", action="store_true", help="Запуск в режиме GUI вместо командной строки")

    parser.add_argument('-jp', '--json-path', help='Путь до .json файла с настройками.')
    
    return parser.parse_args()

def main():
    try:
        args = parse_args()

        if args.cli:
            mode = "cli"
        if args.gui:
            mode = "gui"
        
        match mode:
            case "gui":
                gui.run_gui()
            case "cli":
                settings = utils.read_json_file(args.json_path)

                bits = settings.get("bits")
                experiments = settings.get("experiments")
                str_length = settings.get("str_length")
                
                collisions.run_experiments(bits , experiments , str_length)
            
    except Exception as e:
        print(f"Критическая ошибка приложения: {e}")

if __name__ == "__main__":
    main()