import argparse
import json
from key_functions import (generate_symmetric_key, generate_asymmetric_keys, write_public_key, write_private_key, encrypt_symmetric_key,
 write_symmetric_key, read_symmetric_key, read_private_pem, decrypt_symmetric_key)
from cryption_functions import encrypt_text, decrypt_text
from rw_text_functions import read_text_file, write_encrypt_text, read_encrypt_text, write_decrypt_text


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='1. Starts keys generation mode')
    group.add_argument('-enc','--encryption',help='2. Starts encryption mode')
    group.add_argument('-dec','--decryption',help='3. Starts decryption mode')
    
    parser.add_argument('-json', '--settings', default='settings.json', help='path to settings file')

    args = parser.parse_args()

    try:
        with open(args.settings, 'r') as json_file:
            json_data = json.load(json_file)

            initial_file = json_data['initial_file']
            encrypted_file = json_data['encrypted_file']
            decrypted_file = json_data['decrypted_file']
            symmetric_key_file = json_data['symmetric_key']
            public_key_file = json_data['public_key']
            secret_key_file = json_data['secret_key']
        print("Settings are loaded")

    except FileNotFoundError:
        print("Settings file was not found")
    except Exception as error:
        print(f"Error has occurred: {error}")
    
    try:
        if args.generation is not None:
            print("1. Keys generation mode")
            
            key = generate_symmetric_key()
            print("1.1 Key for the symmetric algorithm has been generated")

            private_key, public_key = generate_asymmetric_keys()
            print("1.2 Keys for asymmetric algorithm have been generated")

            write_public_key(public_key, public_key_file)
            print("1.3.1 Public key is serialized in .pem file")

            write_private_key(private_key, secret_key_file)
            print("1.3.2 Private key is serialized in .pem file")

            encrypt_key = encrypt_symmetric_key(key, public_key)
            print("1.4.1 Symmetric encryption key is encrypted with public key")

            write_symmetric_key(encrypt_key, symmetric_key_file)
            print("1.4.2 Encrypted symmetric encryption key is saved in .txt file")
            

        elif args.encryption is not None:
            print("2. Data encryption mode")

            content = read_symmetric_key(symmetric_key_file)
            print("2.1.1 Encrypted symmetric key is read from file")

            private_key = read_private_pem(secret_key_file)
            print("2.1.2 Private key for decrypting symmetric key is read from file")

            key = decrypt_symmetric_key(content, private_key)
            print("2.1.3 Symmetric key has been decrypted")

            text_bytes = read_text_file(initial_file)
            print("2.2.1 Text for encryption is read from file")

            iv, c_text = encrypt_text(text_bytes, key)
            print("2.2.2 Text was encrypted using SM4 algorithm")

            write_encrypt_text(encrypted_file, iv, c_text)
            print("2.2.3 Encrypted text was written to file")
            

        else:
            print("3. Data decryption mode")

            content = read_symmetric_key(symmetric_key_file)
            print("3.1.1 Encrypted symmetric key is read from file")

            private_key = read_private_pem(secret_key_file)
            print("3.1.2 Private key for decrypting symmetric key is read from file")

            key = decrypt_symmetric_key(content, private_key)
            print("3.1.3 Symmetric key has been decrypted")

            iv, c_text = read_encrypt_text(encrypted_file)
            print("3.2.1 Encrypted text is read from file")

            dc_text = decrypt_text(iv, c_text, key)
            print("3.2.2 Text has been decrypted")

            write_decrypt_text(decrypted_file, dc_text)
            print("3.2.3 Decrypted text was written to file")
             
    except Exception as error:
        print(f"Error has occurred: {error}")

if __name__ == "__main__" :
    main()