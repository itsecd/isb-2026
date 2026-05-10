import argparse
import sys

from auxiliary_functions import load_settings
from asymmetrical import generate_rsa_keys, save_rsa_keys, encrypt_symmetric_key, decrypt_symmetric_key
from symmetrical import generate_symmetric_key, encrypt_data, decrypt_data

def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gen', action='store_true', help='Генерация ключей')
    group.add_argument('--enc', action='store_true', help='Шифрование данных')
    group.add_argument('--dec', action='store_true', help='Дешифрование данных')
    
    parser.add_argument('--settings', type=str, default='settings.json', help='Путь к файлу настроек JSON')

    args = parser.parse_args()
    settings = load_settings(args.settings)

    match True:
        case _ if args.gen:
            symmetric_key = generate_symmetric_key(settings)
            if symmetric_key is None:
                return
            
            private_key, public_key = generate_rsa_keys(settings)
            if private_key is None or public_key is None:
                return
            
            if not save_rsa_keys(settings, private_key, public_key):
                return
            
            if encrypt_symmetric_key(settings, symmetric_key) is None:
                return
            
            print("Генерация ключей завершена")
            
        case _ if args.enc:
            symmetric_key = decrypt_symmetric_key(settings)
            if symmetric_key is None:
                return
            print(f"Симметричный ключ расшифрован")
            
            if not encrypt_data(settings, symmetric_key):
                return
                
        case _ if args.dec:
            symmetric_key = decrypt_symmetric_key(settings)
            if symmetric_key is None:
                return
            print(f"Симметричный ключ расшифрован")
            
            if not decrypt_data(settings, symmetric_key):
                return

if __name__ == '__main__':
    main()