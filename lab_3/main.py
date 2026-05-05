import sys
import json
import argparse
from gen_key import *


def load_settings(filepath: str):
    try:
        with open('settings.json') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        raise 


def parse_args() -> argparse.Namespace:
    """
    Parse parameters from console.
    """
    parser = argparse.ArgumentParser (description="Hybrid cryptosystem:" )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--gen', action='store_true', help='Run key generation mode to create RSA key pair and symmetric key')
    group.add_argument('-e', '--enc', action='store_true', help='Run encryption mode to encrypt input file using symmetric key and RSA')
    group.add_argument('-d', '--dec', action='store_true', help='Run decryption mode to decrypt input file using symmetric key and RSA')

    parser.add_argument('-k', '--key-size', type=int, default=128, help='Set symmetric key length in bits from 32 to 448 with step of 8')
    parser.add_argument('-so', '--sym-key-out', default='keys/sym_key.enc', help='Output path for encrypted symmetric key file')
    parser.add_argument('-pu', '--pub-key-out', default='keys/public.pem', help='Output path for generated RSA public key file')
    parser.add_argument('-pr', '--priv-key-out', default='keys/private.pem', help='Output path for generated RSA private key file')

    parser.add_argument('-i', '--in-file', help='Path to input file for encryption or decryption')
    parser.add_argument('-o', '--out-file', help='Path to output file for result of encryption or decryption')
    parser.add_argument('-pk', '--priv-key-file', help='Path to RSA private key file used for decryption process')
    parser.add_argument('-sk', '--sym-key-file', help='Path to encrypted symmetric key file used in encryption or decryption')

    parser.add_argument('-c', '--config', default='settings.json', help='Path to JSON configuration file with program settings')
    args = parser.parse_args()




def main() -> None:
    try:
        args = parse_args()
        settings = load_settings(args.settings)

        if args.gen is None:
            print("Generate keys...")
            symmetric_key = generate_symmetric_key(args.key_size)
            private_key, public_key = generate_rsa_keys()

            save_symmetric_key(symmetric_key, args.sym_key_out)
            print(f"The symmetric key is saved", )
            save_public_key(public_key, args.pub_key_out)
            print(f"The public key is saved", )
            save_private_key(private_key, args.priv_key_out)
            print(f"The private key is saved", )

        elif args.enc is None:
            print("ENCRYPTING")
        else: 
            print("DECRYPTING")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main ()