import argparse
import asym
import sym
import keygen
import util


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

    group2 = parser.add_mutually_exclusive_group(required = True)
    group2.add_argument('-cam','--camellia',help='Использование алгоритма Camellia')
    group2.add_argument('-aes','--aes',help='Использование алгоритма AES')

    parser.add_argument('-jp', '--json_path', help='Путь до .json файла с настройками.')
    

    return parser.parse_args()


def main():
    try:
        args = parse_args()
        json_settings = util.read_json_file(args.json_path)

        init_file_path = json_settings.get("initial_file")
        ciph_file_path = json_settings.get("cipher_text")
        dec_file_path = json_settings.get("decrypted_file")
        sym_key_path = json_settings.get("symmetric_key")
        pub_key_path = json_settings.get("public_key")
        sec_key_path = json_settings.get("secret_key")
        key_length = int(json_settings.get("key_length"))

        if args.generation:
            mode = "generation"
        else:
            c_sym_key = util.read_file(sym_key_path)
            sym_key = asym.decrypt_with_private_key(c_sym_key, sec_key_path)
            if args.encryption:
                mode = "encryption"
            else:
                mode = "decryption"
        if args.camellia:
            algo = "camellia"
        if args.aes:
            algo = "aes"
        match algo:
            case "camellia":
                match mode:
                    case "generation":
                        sym_key = keygen.volshebniy_kluch(key_length)
                        keygen.asym_keygen(pub_key_path, sec_key_path)
                        с_sym_key = asym.encrypt_with_public_key(sym_key, pub_key_path)
                        util.write_file(sym_key_path, с_sym_key)
                    case "encryption":
                        c_text = sym.encrypt_data_camellia(init_file_path, sym_key)
                        util.write_file(ciph_file_path, c_text)
                    case "decryption":
                        dc_text = sym.decrypt_data_camellia(ciph_file_path, sym_key)
                        util.write_file(dec_file_path, dc_text)
            case "aes":
                    match mode:
                        case "generation":
                            sym_key = keygen.volshebniy_kluch(key_length)
                            keygen.asym_keygen(pub_key_path, sec_key_path)
                            с_sym_key = asym.encrypt_with_public_key(sym_key, pub_key_path)
                            util.write_file(sym_key_path, с_sym_key)
                        case "encryption":
                            c_text = sym.encrypt_data_aes(init_file_path, sym_key)
                            util.write_file(ciph_file_path, c_text)
                        case "decryption":
                            dc_text = sym.decrypt_data_aes(ciph_file_path, sym_key)
                            util.write_file(dec_file_path, dc_text)
        
            
    except Exception as e:
        print(f"В ходе работы произошла ошибка {e}")     
            
if __name__ == "__main__":
    main()