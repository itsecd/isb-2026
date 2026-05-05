import json
from logic import enc_logic, dec_logic, gen_logic

import argparse


def parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',type = int, help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',action='store_true',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',action='store_true',help='Запускает режим дешифрования')
    args = parser.parse_args()
    return args
    

def json_parser() -> dict:
    try:
        with open("settings.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as ex:
        print(f"Ошибка!: {ex}")


def main():
    action = parser()
    settings = json_parser()
    match action:
        case _ if action.encryption:
            enc_logic(settings)
        case _ if action.decryption:
            dec_logic(settings)
        case _ if action.generation is not None:
            match action.generation:
                case 64:
                    gen_logic(settings, action.generation)
                case 128:
                    gen_logic(settings, action.generation)
                case 192:
                    gen_logic(settings, action.generation)
                case _:
                    print("Некорректная длинна ключа")

if __name__ == "__main__":
    main()