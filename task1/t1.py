import argparse
import os
import caeser


def read_file(file_path: str) -> str:
    """Read and return the content of a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    """Write content to a text file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_key_from_args(args) -> int:
    """Extract encryption key from command line arguments."""
    if args.key is not None:
        return args.key

    if not os.path.exists(args.key_file):
        raise FileNotFoundError(f"Key file {args.key_file} not found.")

    with open(args.key_file, 'r', encoding='utf-8') as f:
        key_str = f.read().strip()
        try:
            return int(key_str)
        except ValueError:
            raise ValueError(f"Key file {args.key_file} must contain an integer.")


def main():
    parser = argparse.ArgumentParser(description='Encrypt text using Caesar cipher.')
    parser.add_argument('--input', default='text.txt',
                        help='input text file (default: text.txt)')
    parser.add_argument('--output', default='encrypted.txt',
                        help='output file for encrypted text (default: encrypted.txt)')
    parser.add_argument('--key', type=int,
                        help='shift key (integer). If omitted, read from --key-file')
    parser.add_argument('--key-file', default='key.txt',
                        help='file containing the key (default: key.txt); used only if --key not given')
    args = parser.parse_args()

    try:
        key = get_key_from_args(args)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    if not os.path.exists(args.input):
        print(f"Error: input file {args.input} not found.")
        return

    try:
        plaintext = read_file(args.input)
        ciphertext = caeser.encrypt(plaintext, key)
        write_file(args.output, ciphertext)
        print(f"Encryption completed. Result saved to {args.output}")

        decrypted = caeser.decrypt(ciphertext, key)
        if plaintext.upper() == decrypted:
            print("Decryption check passed: decrypted text matches original.")
        else:
            print("Decryption check failed: decrypted text does not match original.")
    except Exception as e:
        print(f"Encryption failed: {e}")


if __name__ == '__main__':
    main()