import argparse
import os
import json
from file_utils import read_json_file, settings_validation_check, write_file_bytes, read_file_bytes, read_initial_text, write_decrypted_text, write_public_key, write_private_key, read_public_key, read_private_key
from symmetrical import gen_sym_key, triple_des_encryption, triple_des_decryption
from asymmetrical import gen_assym_key, rsa_encryption, rsa_decryption


def decription_cut(file_sym_key: str, file_priv_key: str) -> bytes:
    c_key = read_file_bytes(file_sym_key, mode='key')
    private_key = read_private_key(file_priv_key)
    sym_key = rsa_decryption(c_key, private_key)
    return sym_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings', help='The name of the setting file', default='settings.json')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen', '--generation', action='store_const', const='gen', dest='mode', help='Starts the key generation mode')
    group.add_argument('-enc', '--encryption', action='store_const', const='enc', dest='mode', help='Starts the encryption mode')
    group.add_argument('-dec', '--decryption', action='store_const', const='dec', dest='mode', help='Starts the decryption mode')
    args = parser.parse_args()
    
    try:
        settings = read_json_file(args.settings)
        settings_validation_check(settings)

        match args.mode:
            case 'gen':
                sym_key = gen_sym_key(settings['sym_key_length'])

                public_key, private_key = gen_assym_key()
                write_public_key(settings['public_key'], public_key)
                write_private_key(settings['private_key'], private_key)

                c_sym_key = rsa_encryption(sym_key, public_key)
                write_file_bytes(settings['symmetric_key'], c_sym_key, mode='key')

            case 'enc':
                sym_key = decription_cut(settings['symmetric_key'], settings['private_key'])

                text = read_initial_text(settings['initial_file'])
                c_text, iv = triple_des_encryption(text, sym_key)

                full_data = iv + c_text
                write_file_bytes(settings['encrypted_file'], full_data, mode='text')

            case 'dec':
                sym_key = decription_cut(settings['symmetric_key'], settings['private_key'])

                full_data = read_file_bytes(settings['encrypted_file'], mode='text')
                iv = full_data[:8]
                c_text = full_data[8:]

                text = triple_des_decryption(c_text, sym_key, iv)
                write_file_bytes(settings['decrypted_file'], text, mode="text")
    
    except Exception as e:
        print(f"Error: {e}")