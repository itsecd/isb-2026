import argparse
from file_utils import *
from symmetric import *
from asymmetric import *


def parse_args() -> argparse.Namespace:
    """
    Parses CLI arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Hybrid cryptosystem")

    parser.add_argument(
        '-m', '--mode',
        choices=['gen', 'enc', 'dec'],
        required=True,
        help=(
            "Operation mode:\n"
            "gen - generate RSA and symmetric keys\n"
            "enc - encrypt input file\n"
            "dec - decrypt input file"
        )
    )

    parser.add_argument('-k', '--key-size', type=int, default=256)
    parser.add_argument('-so', '--sym-key-out', default='keys/sym_key.enc')
    parser.add_argument('-pu', '--pub-key-out', default='keys/public.pem')
    parser.add_argument('-pr', '--priv-key-out', default='keys/private.pem')

    parser.add_argument('-i', '--in-file')
    parser.add_argument('-o', '--out-file')
    parser.add_argument('-pk', '--priv-key-file')
    parser.add_argument('-sk', '--sym-key-file')

    parser.add_argument('-c', '--config', default='src/settings.json')

    return parser.parse_args()


def merge_args_with_settings(args, settings: dict):
    """
    Merges CLI arguments with JSON settings (CLI has priority).

    Args:
        args (argparse.Namespace): CLI arguments.
        settings (dict): JSON config.

    Returns:
        argparse.Namespace: Updated arguments.
    """
    for key, value in settings.items():
        if hasattr(args, key) and getattr(args, key) is None:
            setattr(args, key, value)
    return args


def generate_mode(args):
    """
    Generates RSA key pair and symmetric key.

    Args:
        args (argparse.Namespace): CLI arguments.

    Returns:
        None
    """
    try:
        print("Generate keys...")

        sym_key = generate_symmetric_key(args.key_size)
        private_key, public_key = generate_rsa_keys()

        enc_sym_key = encrypt_symmetric_key(sym_key, public_key)

        save_symmetric_key(enc_sym_key, args.sym_key_out)
        save_public_key(public_key, args.pub_key_out)
        save_private_key(private_key, args.priv_key_out)

        print("Successful key generation")

    except Exception as e:
        print(f"Error: {e}")


def encrypt_mode(args):
    """
    Encrypts input file using ChaCha20 + RSA key handling.

    Args:
        args (argparse.Namespace): CLI arguments.

    Returns:
        None
    """
    try:
        print("Encrypting...")

        private_key = load_private_key(args.priv_key_file)

        sym_key = decrypt_symmetric_key(
            args.sym_key_file,
            private_key
        )

        nonce, ciphertext = load_encrypted_file(args.in_file)

        plaintext = chacha20_decrypt(ciphertext, sym_key, nonce)
        
        write_bytes(args.out_file, plaintext)
        print("Successful encrypt")

    except Exception as e:
        print(f"Error: {e}")


def decrypt_mode(args):
    """
    Decrypts encrypted file using ChaCha20 + RSA.

    Args:
        args (argparse.Namespace): CLI arguments.

    Returns:
        None
    """
    try:
        print("Decrypting...")

        private_key = load_private_key(args.priv_key_file)

        symmetric_key = decrypt_symmetric_key(
            args.sym_key_file,
            private_key
        )

        nonce, cipher_text = load_encrypted_file(args.in_file)

        plaintext = chacha20_decrypt(cipher_text, symmetric_key, nonce)

        write_bytes(args.out_file, plaintext)

        print("Successful decrypt")

    except Exception as e:
        print(f"Error: {e}")