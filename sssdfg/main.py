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

        if args.generation is not None:
            print("Топор+")
        elif args.encryption is not None:
            print("Поздняков подписаться")
        else:
            print("Думайте")   
        
    except Exception as e:
        print("Увынск Топор+ подписаться:", e)     
            
if __name__ == "__main__":
    main()
            
if __name__ == "__main__":
    main()
