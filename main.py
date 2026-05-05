import json
from logic import enc_logic, dec_logic, gen_logic

import argparse


def parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',help='Запускает режим дешифрования')
    settings = json_parser()
    args = parser.parse_args()
    if args.generation is not None:
        return gen_logic(settings)
    elif args.encryption is not None:
        return enc_logic(settings)
    else:
        return dec_logic(settings)

def json_parser() -> dict:
    try:
        with open("settings.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as ex:
        print(f"Ошибка!: {ex}")


def main():
    parser()
    settings = json_parser()
    action = str(input("Выберите действие(enc/dec/gen/exit):"))
    while(action != "exit"):
        if action == "enc":
            enc_logic(settings)
        elif action == "dec":
            dec_logic(settings)
        elif action == "gen":
            gen_logic(settings)
        action = str(input("Выберите действие(enc/dec/gen/exit):"))
    return 0

if __name__ == "__main__":
    main()