import argparse
import json
from file_utils import read_binary_file, write_binary_file, generate_random_bytes
from symmetric_crypto import AESCipher, generate_aes_key
from asymmetric_crypto import RSAKeyPair

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование')
    group.add_argument('-dec', '--decryption', action='store_true', help='Дешифрование')
    
    parser.add_argument('--key-size', type=int, default=256, choices=[128, 192, 256],
                        help='Размер ключа AES в битах (по умолчанию 256)')
    
    args = parser.parse_args()

    settings = load_settings()

    if args.generation:
        print("[*] Режим генерации ключей...")
        sym_key = generate_aes_key(args.key_size)
        print(f"  Сгенерирован симметричный ключ AES ({args.key_size} бит)")

        rsa_keys = RSAKeyPair()
        rsa_keys.save_to_files(
            settings.get('secret_key', 'private_key.pem'),
            settings.get('public_key', 'public_key.pem')
        )
        print(f"  Сохранены RSA-ключи")

        enc_sym_key = rsa_keys.encrypt_symmetric_key(sym_key)
        write_binary_file(settings.get('symmetric_key', 'symmetric_key.bin'), enc_sym_key)
        print(f"  Зашифрованный симметричный ключ сохранён")

    elif args.encryption:
        print("[*] Режим шифрования...")
        
        rsa_keys = RSAKeyPair.load_from_files(
            settings.get('secret_key', 'private_key.pem'),
            settings.get('public_key', 'public_key.pem')
        )
        enc_sym_key = read_binary_file(settings.get('symmetric_key', 'symmetric_key.bin'))
        sym_key = rsa_keys.decrypt_symmetric_key(enc_sym_key)
        print("  Симметричный ключ расшифрован")
      
        plaintext = read_binary_file(settings.get('initial_file', 'input.txt'))
        print(f"  Прочитано {len(plaintext)} байт")

        iv = generate_random_bytes(16)
        cipher = AESCipher(sym_key)
        ciphertext = cipher.encrypt(plaintext, iv)

        write_binary_file(settings.get('encrypted_file', 'encrypted.bin'), iv + ciphertext)
        print("  Данные зашифрованы и сохранены")

    elif args.decryption:
        print("[*] Режим дешифрования...")
        rsa_keys = RSAKeyPair.load_from_files(
            settings.get('secret_key', 'private_key.pem'),
            settings.get('public_key', 'public_key.pem')
        )
        enc_sym_key = read_binary_file(settings.get('symmetric_key', 'symmetric_key.bin'))
        sym_key = rsa_keys.decrypt_symmetric_key(enc_sym_key)
        print("  Симметричный ключ расшифрован")

        encrypted_data = read_binary_file(settings.get('encrypted_file', 'encrypted.bin'))
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        cipher = AESCipher(sym_key)
        plaintext = cipher.decrypt(ciphertext, iv)

        write_binary_file(settings.get('decrypted_file', 'decrypted.txt'), plaintext)
        print("  Данные расшифрованы и сохранены")

if __name__ == "__main__":
    main()
