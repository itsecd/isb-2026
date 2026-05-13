import argparse
import os
import json
import file_utils

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
                pass
            case 'enc':
                pass
            case 'dec':
                pass
    
    except Exception as e:
        print(f"Error: {e}")