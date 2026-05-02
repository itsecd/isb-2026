import argparse

import generate_key
import symmetric
import asymmetric
import load_and_save_data

def get_args():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема (RSA + CAST5)")
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-gen', '--generation', action='store_true', help='Режим генерации ключей')
    mode_group.add_argument('-enc', '--encryption', action='store_true', help='Режим шифрования данных')
    mode_group.add_argument('-dec', '--decryption', action='store_true', help='Режим дешифрования данных')

    parser.add_argument('--init', type=str, help='Путь к исходному текстовому файлу')
    parser.add_argument('--enc_file', type=str, help='Путь для сохранения/чтения зашифрованных данных')
    parser.add_argument('--dec_file', type=str, help='Путь для сохранения расшифрованного текста')
    parser.add_argument('--sym', type=str, help='Путь к зашифрованному симметричному ключу')
    parser.add_argument('--pub', type=str, help='Путь к открытому ключу RSA')
    parser.add_argument('--priv', type=str, help='Путь к закрытому ключу RSA')
    parser.add_argument('--settings', type=str, default='settings.json', help='Путь к файлу конфигурации (по умолчанию settings.json)')
    parser.add_argument('--key_len', type=int, choices=range(40, 136, 8), default=128, help='Длина ключа CAST5 в битах (от 40 до 128 с шагом 8)')
    
    return parser.parse_args()

def get_settings() -> dict:
    args = get_args()
    config = load_and_save_data.load_json(args.settings)

    final_config = {
        "mode": "gen" if args.generation else "enc" if args.encryption else "dec",
        "initial_file": args.init or config.get("initial_file", "message.txt"),
        "encrypted_file": args.enc_file or config.get("encrypted_file", "encrypted.bin"),
        "decrypted_file": args.dec_file or config.get("decrypted_file", "decrypted.txt"),
        "symmetric_key": args.sym or config.get("symmetric_key", "sym_key.enc"),
        "public_key": args.pub or config.get("public_key", "public.pem"),
        "private_key": args.priv or config.get("private_key", "private.pem"),
        "key_len": args.key_len
    }
    return final_config

def main():
    config = get_settings()

    if config["mode"] == "gen":
        private_key, public_key = generate_key.generating_asymmetric_key()
        load_and_save_data.save_asym_keys(private_key, public_key, config["private_key"], config["public_key"])
       
    elif config["mode"] == "enc":
        public_key = load_and_save_data.load_public_key(config["public_key"])
        sym_key = generate_key.generating_symmetric_key(config["key_len"] // 8)  
        text = load_and_save_data.read_text_file(config["initial_file"])
        encrypt_text_bytes = symmetric.encrypt_text(text, sym_key)
        encrypt_sym_key = asymmetric.encrypt_symmetric_key(sym_key, public_key)
        load_and_save_data.save_symmetric_key(encrypt_sym_key, config["symmetric_key"])
        load_and_save_data.write_binary_file(encrypt_text_bytes, config["encrypted_file"])
        
    elif config["mode"] == "dec":
        private_key = load_and_save_data.load_private_key(config["private_key"])
        sym_key_encrypted = load_and_save_data.load_encrypt_symmetric_key(config["symmetric_key"])
        sym_key = asymmetric.decrypt_key(sym_key_encrypted, private_key)
        encrypted_text = load_and_save_data.read_binary_file(config["encrypted_file"])
        decrypted_text = symmetric.decrypt_text(encrypted_text, sym_key)
        load_and_save_data.write_text_file(decrypted_text, config["decrypted_file"])

if __name__ == "__main__":
    main()