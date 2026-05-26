import argparse
import json
from key_functions import (
    generate_symmetric_key, generate_asymmetric_keys, write_public_key,
    write_private_key, encrypt_symmetric_key, write_symmetric_key,
    read_symmetric_key, read_private_pem, decrypt_symmetric_key
)
from cryption_functions import encrypt_text, decrypt_text
from rw_text_functions import (
    read_text_file, write_encrypt_text, read_encrypt_text, write_decrypt_text
)

def load_settings(settings_path: str) -> dict:
    """
    Load settings from JSON file
    """
    try:
        with open(settings_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        print("Settings are loaded")
        return json_data
    except FileNotFoundError:
        raise FileNotFoundError(f"{settings_path} file was not found")
    except Exception as e:
        raise Exception(f"Failed to load settings from {settings_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Гибридная криптосистема (RSA + AES)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='1. Starts keys generation mode')
    group.add_argument('-enc', '--encryption', help='2. Starts encryption mode')
    group.add_argument('-dec', '--decryption', help='3. Starts decryption mode')
    group.add_argument('-config', '--configure', help='4. Starts configuration mode')

    parser.add_argument('-json', '--settings', default='settings.json', help='path to settings file')

    args = parser.parse_args()

    try:
        with open(args.settings, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

            initial_file = json_data['initial_file']
            encrypted_file = json_data['encrypted_file']
            decrypted_file = json_data['decrypted_file']
            symmetric_key_file = json_data['symmetric_key']
            public_key_file = json_data['public_key']
            private_key_file = json_data['private_key']
            aes_key_size = json_data.get('aes_key_size', 256)
        
        print("Settings are loaded")

    except FileNotFoundError:
        print(f"Settings file {args.settings} was not found")
        return
    except Exception as error:
        print(f"Error has occurred while loading settings: {error}")
        return
    try:
        match args:
            case _ if args.generation:
                print("\n1. Keys generation mode")
                print("="*50)

                key = generate_symmetric_key(aes_key_size)
                print("1.1 Key for the symmetric algorithm has been generated")

                private_key, public_key = generate_asymmetric_keys()
                print("1.2 Keys for asymmetric algorithm have been generated")

                write_public_key(public_key, public_key_file)
                print("1.3.1 Public key is serialized in .pem file")

                write_private_key(private_key, private_key_file)
                print("1.3.2 Private key is serialized in .pem file")

                encrypt_key = encrypt_symmetric_key(key, public_key)
                print("1.4.1 Symmetric encryption key is encrypted with public key")

                write_symmetric_key(encrypt_key, symmetric_key_file)
                print("1.4.2 Encrypted symmetric encryption key is saved in file")

                print("\n" + "="*50)
                print("KEYS GENERATION COMPLETED SUCCESSFULLY")

            case _ if args.encryption:
                print("\n2. Data encryption mode")
                print("="*50)

                content = read_symmetric_key(symmetric_key_file)
                print("2.1.1 Encrypted symmetric key is read from file")

                private_key = read_private_pem(private_key_file)
                print("2.1.2 Private key for decrypting symmetric key is read from file")

                key = decrypt_symmetric_key(content, private_key)
                print("2.1.3 Symmetric key has been decrypted")

                text_bytes = read_text_file(initial_file)
                print("2.2.1 Text for encryption is read from file")

                iv, c_text = encrypt_text(text_bytes, key, aes_key_size)
                print("2.2.2 Text was encrypted using AES algorithm")

                write_encrypt_text(encrypted_file, iv, c_text)
                print("2.2.3 Encrypted text was written to file")

                print("\n" + "="*50)
                print("ENCRYPTION COMPLETED SUCCESSFULLY")

            case _ if args.decryption:
                print("\n3. Data decryption mode")
                print("="*50)

                content = read_symmetric_key(symmetric_key_file)
                print("3.1.1 Encrypted symmetric key is read from file")

                private_key = read_private_pem(private_key_file)
                print("3.1.2 Private key for decrypting symmetric key is read from file")

                key = decrypt_symmetric_key(content, private_key)
                print("3.1.3 Symmetric key has been decrypted")

                iv, c_text = read_encrypt_text(encrypted_file)
                print("3.2.1 Encrypted text is read from file")

                dc_text = decrypt_text(iv, c_text, key, aes_key_size)
                print("3.2.2 Text has been decrypted")

                write_decrypt_text(decrypted_file, dc_text)
                print("3.2.3 Decrypted text was written to file")

                print("\n" + "="*50)
                print("DECRYPTION COMPLETED SUCCESSFULLY")

            case _ if args.configure:
                print("\n4. Configuration mode")
                print("="*50)
                
                print(f"Current AES key size: {aes_key_size} bits")
                new_size = input("Enter new AES key size (128/192/256) or press Enter to keep current: ")
                
                if new_size:
                    aes_key_size = int(new_size)
                    json_data['aes_key_size'] = aes_key_size
                    
                    with open(args.settings, 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                    print(f"AES key size updated to {aes_key_size} bits")
                
                print("\n" + "="*50)
                print("CONFIGURATION COMPLETED")

    except FileNotFoundError as error:
        print(f"File not found error: {error}")
    except ValueError as error:
        print(f"Value error: {error}")
    except Exception as error:
        print(f"Error has occurred: {error}")


if __name__ == "__main__":
    main()
    
    