import sys
import argparse
from gen_key import *
from encrypt import *
from decrypt import *
from file_utils import *


def parse_args() -> argparse.Namespace:
    """
    Parse parameters from console.
    """
    parser = argparse.ArgumentParser (description="Hybrid cryptosystem:" )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--gen', action='store_true', help='Run key generation mode to create RSA key pair and symmetric key')
    group.add_argument('-e', '--enc', action='store_true', help='Run encryption mode to encrypt input file using symmetric key and RSA')
    group.add_argument('-d', '--dec', action='store_true', help='Run decryption mode to decrypt input file using symmetric key and RSA')

    parser.add_argument('-k', '--key-size', type=int, default=256, help='Set symmetric key length in bits from 32 to 448 with step of 8')
    parser.add_argument('-so', '--sym-key-out', default='keys/sym_key.enc', help='Output path for encrypted symmetric key file')
    parser.add_argument('-pu', '--pub-key-out', default='keys/public.pem', help='Output path for generated RSA public key file')
    parser.add_argument('-pr', '--priv-key-out', default='keys/private.pem', help='Output path for generated RSA private key file')

    parser.add_argument('-i', '--in-file', help='Path to input file for encryption or decryption')
    parser.add_argument('-o', '--out-file', help='Path to output file for result of encryption or decryption')
    parser.add_argument('-pk', '--priv-key-file', help='Path to RSA private key file used for decryption process')
    parser.add_argument('-sk', '--sym-key-file', help='Path to encrypted symmetric key file used in encryption or decryption')

    parser.add_argument('-c', '--config', default='src/settings.json', help='Path to JSON configuration file with program settings')
    return parser.parse_args()


def merge_args_with_settings(args, settings: dict):
    for key, value in settings.items():
        if hasattr(args, key):
            if getattr(args, key) is None:
                setattr(args, key, value)
    return args


def main() -> None:
    try:
        args = parse_args()
        settings = load_settings(args.config)
        args = merge_args_with_settings(args, settings)

        if args.gen:
            print("Generate keys...")

            sym_key = generate_symmetric_key(args.key_size)
            private_key, public_key = generate_rsa_keys()

            encrypted_sym_key = public_key.encrypt(
                sym_key,
                asymmetric_padding.OAEP(
                    mgf=asymmetric_padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            save_symmetric_key(encrypted_sym_key, args.sym_key_out)
            save_public_key(public_key, args.pub_key_out)
            save_private_key(private_key, args.priv_key_out)
            print("Succeseful")
        elif args.enc:
                print("Encrypting...")

                private_key = load_private_key(args.priv_key_file)

                sym_key = decrypt_symmetric_key(
                    args.sym_key_file,
                    private_key
                )

                nonce, ciphertext = load_encrypted_file(args.in_file)

                plaintext = chacha20_decrypt(ciphertext, sym_key, nonce)

                with open(args.out_file, 'wb') as f:
                    f.write(plaintext)
                print("Succeseful")
        else: 
            print("DECRYPTING")

            private_key = load_private_key(args.priv_key_file)

            symmetric_key = decrypt_symmetric_key(
                args.sym_key_file,
                private_key
            )

            nonce, cipher_text = load_encrypted_file(args.in_file)

            plaintext = chacha20_decrypt(cipher_text, symmetric_key, nonce)

            
            with open(args.out_file, 'wb') as f:
                f.write(plaintext)

            print("Successful")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main ()