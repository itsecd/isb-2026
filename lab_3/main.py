import json
from logic import enc_logic, dec_logic, gen_logic
import argparse
from load_and_save import load_settings

def parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',type = int, help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',action='store_true',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',action='store_true',help='Запускает режим дешифрования')
    parser.add_argument('input', nargs='?', help='Путь к исходному файлу')
    parser.add_argument('output', nargs='?', help='Путь к файлу результата')
    args = parser.parse_args()
    return args

def main():
    action = parser()
    settings = load_settings()
    input_path = action.input
    output_path = action.output
    match action:
        case _ if action.encryption:
            match input_path:
                case None:
                    input_path = settings["initial_file_path"]
            match output_path:
                case None:
                    output_path = settings["encrypted_file_path"]
            enc_logic(settings, input_path, output_path)
        case _ if action.decryption:
            match input_path:
                case None:
                    input_path = settings["encrypted_file_path"]
            match output_path:
                case None:
                    output_path = settings["decrypted_file_path"]
            dec_logic(settings, input_path, output_path)
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
