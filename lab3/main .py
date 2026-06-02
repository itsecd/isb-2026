"""
Main entry point for hybrid cryptosystem command-line interface.

Provides three operational modes:
- Key generation: creates RSA keys and encrypts a symmetric key
- Encryption: encrypts files using hybrid cryptosystem
- Decryption: decrypts files using hybrid cryptosystem

Usage examples:
    python main.py -gen -s encrypted.key -p public.pem -r private.pem
    python main.py -enc -i plain.txt -k private.pem -s encrypted.key -o encrypted.bin
    python main.py -dec -i encrypted.bin -k private.pem -s encrypted.key -o decrypted.txt
"""

import argparse
import sys
from key_generator import generate_keys
from encryptor import encrypt_file
from decryptor import decrypt_file
from exceptions import (
    KeyGenerationError,
    KeyLoadError,
    EncryptionError,
    DecryptionError,
    FileOperationError,
    PaddingError,
)


def parse_args():
    """
    Parse command-line arguments for the hybrid cryptosystem.

    Defines three mutually exclusive operation modes (-gen, -enc, -dec)
    with corresponding required arguments for each mode.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing:
            - generation, encryption, decryption: Mode flags
            - input: Input file path
            - output: Output file path
            - symmetric: Encrypted symmetric key file path
            - public: Public key (.pem) path
            - private/private: Private key (.pem) path

    Command-line syntax:
        -gen      Generate keys: requires -s, -p, -r
        -enc      Encrypt file: requires -i, -k/-r, -s, -o
        -dec      Decrypt file: requires -i, -k/-r, -s, -o
        -i/--input       Input file path
        -o/--output      Output file path
        -s/--symmetric   Encrypted symmetric key path
        -p/--public      Public key (.pem) path
        -r/--private     Private key (.pem) path
        -k/--key         Alias for -r
    """
    parser = argparse.ArgumentParser(
        description="Hybrid Crypto System (RSA + SEED-128)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true", help="Run key generation mode")
    group.add_argument("-enc", "--encryption", action="store_true", help="Run encryption mode")
    group.add_argument("-dec", "--decryption", action="store_true", help="Run decryption mode")

    parser.add_argument("-i", "--input",     help="Input file path")
    parser.add_argument("-o", "--output",    help="Output file path")
    parser.add_argument("-s", "--symmetric", help="Encrypted symmetric key path")
    parser.add_argument("-p", "--public",    help="Public key path (.pem)")
    parser.add_argument("-r", "--private",   help="Private key path (.pem)")
    parser.add_argument("-k", "--key",       help="Private key path (alias for -r)")

    return parser.parse_args()


def main():
    """
    Main entry point for the hybrid cryptosystem CLI.

    Routes execution to appropriate handler based on operation mode.
    Includes comprehensive error handling for all crypto-related exceptions.

    Returns:
        int: Exit code (0 for success, 1 for error).

    Modes:
        generation: Calls generate_keys() to create RSA key pair and encrypted symmetric key.
        encryption: Calls encrypt_file() to encrypt a plaintext file.
        decryption: Calls decrypt_file() to decrypt an encrypted file.
    """
    args = parse_args()

    try:
        match True:
            case _ if args.generation:
                if not all([args.symmetric, args.public, args.private]):
                    print("Error: -gen requires -s, -p, and -r arguments.", file=sys.stderr)
                    sys.exit(1)
                generate_keys(
                    encrypted_symmetric_key_path=args.symmetric,
                    public_key_path=args.public,
                    private_key_path=args.private,
                )

            case _ if args.encryption:
                private_key = args.key or args.private
                if not all([args.input, private_key, args.symmetric, args.output]):
                    print("Error: -enc requires -i, -k/-r, -s, and -o arguments.", file=sys.stderr)
                    sys.exit(1)
                encrypt_file(
                    input_path=args.input,
                    private_key_path=private_key,
                    encrypted_symmetric_key_path=args.symmetric,
                    output_path=args.output,
                )

            case _ if args.decryption:
                private_key = args.key or args.private
                if not all([args.input, private_key, args.symmetric, args.output]):
                    print("Error: -dec requires -i, -k/-r, -s, and -o arguments.", file=sys.stderr)
                    sys.exit(1)
                decrypt_file(
                    encrypted_input_path=args.input,
                    private_key_path=private_key,
                    encrypted_symmetric_key_path=args.symmetric,
                    output_path=args.output,
                )

    except (KeyGenerationError, KeyLoadError, EncryptionError, DecryptionError, PaddingError, FileOperationError) as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[INFO] Operation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())