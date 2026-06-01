import argparse
import sys
from key_generator import generate_keys
from encryptor import encrypt_file
from decryptor import decrypt_file


def parse_args():
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
    args = parse_args()

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


if __name__ == "__main__":
    main()
