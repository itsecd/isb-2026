import argparse
import json


def parse_args():
    """
    Парсинг аргументов командной строки:
    -Выбор 1-го из 3-ёх режимов работы программы на выбор
    -Путь до .json файла с настройками
    -sdfkaiubsgahiubkajhgbkajghb
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',help='Запускает режим дешифрования')

    parser.add_argument('-jp', '--json_path', help='Путь до .json файла с настройками.')

    return parser.parse_args()


def read_json_file(filepath: str) -> dict:
    """
    """
    with open(filepath, 'r') as fp:
        json_data = json.load(fp)
    return json_data


def main():
    try:
        json_settings = read_json_file("setting.json")
        args = parse_args()

        if args.generation:
            mode = 1
        else:
            if args.encryption:
                mode = 2
            else:
                if args.decryption:
                    mode = 3    
        
        match mode:
                case 1:
                    print("Топор+")
                case 2:
                    print("Поздняков подписаться")
                case 3:
                    print("Думайте")  
                case _:
                    print("кто прочитал тот здохнет)")
    except Exception as e:
        print("Увынск продолжение смотреть в телеграмм канале Топор+:", e)     
            
if __name__ == "__main__":
    main()
