import argparse
import json
import asym
import sym
import keygen


def parse_args():
    """
    Парсинг аргументов командной строки:
    -Выбор 1-го из 3-ёх режимов работы программы на выбор
    -Путь до .json файла с настройками
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
    Чтение .json файла по указанному пути в словарь.
    На вход принимает путь до .json файла.
    """
    try:
        with open(filepath, 'r') as fp:
            json_data = json.load(fp)
        return json_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {filepath}, увы")


def main():
    try:
        args = parse_args()
        json_settings = read_json_file(args.j)

        init_file_path = json_settings.get("initial_file")
        ciph_file_path = json_settings.get("cipher_text")
        dec_file_path = json_settings.get("decrypted_file")
        sym_key_path = json_settings.get("symmetric_key")
        pub_key_path = json_settings.get("public_key")
        sec_key_path = json_settings.get("secret_key")
        key_length = int(json_settings.get("key_length"))

        if args.generation is not None:
            sym_key = keygen.volshebniy_kluch(key_length)
            keygen.asym_keygen(pub_key_path, sec_key_path)
            sym_key = asym.encrypt_with_public_key(sym_key, pub_key_path)
            with open(sym_key_path, 'wb') as sym_key_file:
                sym_key_file.write(sym_key)

        elif args.encryption is not None:
            with open(sym_key_path, mode='rb') as key_file: 
                c_sym_key = key_file.read()
            sym_key = asym.decrypt_with_private_key(c_sym_key, sec_key_path)
            c_text = sym.encrypt_data(init_file_path, sym_key)
            with open(ciph_file_path, 'wb') as c_file:
                c_file.write(c_text)
        else:
            with open(sym_key_path, mode='rb') as key_file: 
                c_sym_key = key_file.read()
            sym_key = asym.decrypt_with_private_key(c_sym_key, sec_key_path)
            dc_text = sym.decrypt_data(ciph_file_path, sym_key)
            with open(dec_file_path, "wb") as dc_file:
                dc_file.write(dc_text)
        
    except Exception as e:
        print("Увынск Топор+ подписаться:", e)     
            
if __name__ == "__main__":
    main()