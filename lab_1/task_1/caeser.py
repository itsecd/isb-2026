import argparse
import os.path

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "


def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line    arguments

    :return: Parsed command-line arguments namespace containing decrypt flag
    """
    parser = argparse.ArgumentParser(description="Decryption option.")
    parser.add_argument('--decrypt', '-d', action='store_true', default=False, help='Decrypt text for verifying.')
    return parser.parse_args()


def caesar_cipher(text: str, shift: int, mode: str) -> str:
    """
    Encrypt or decrypt text using Caesar cipher

    :param text: Input text to process
    :param shift: Shift for Caesar cipher
    :param mode: Choose encrypt or decrypt
    :return: Processed text
    """
    text = text.upper()
    text = text.replace('Ё', 'Е')

    if mode == 'decrypt':
        shift = -shift

    result = ""
    for char in text:
        if char in ALPHABET:
            old_index = ALPHABET.index(char)
            new_index = (old_index + shift) % len(ALPHABET)
            result += ALPHABET[new_index]
        else:
            result += char

    return result


def main() -> None:
    """
    Main function
    """
    args = parse_arguments()

    data_dir = 'data'
    key_txt = os.path.join(data_dir, 'key.txt')
    input_txt = os.path.join(data_dir, 'input.txt')
    encrypted_txt = os.path.join(data_dir, 'encrypt.txt')

    try:
        with open(key_txt, 'r', encoding='utf-8') as file:
            shift = int(file.read().strip())
    except FileNotFoundError:
        print(f"File with key not found at: {key_txt}")
        return
    except ValueError:
        print(f"File {key_txt} contains invalid shift")
        return

    # flag -d to decrypt
    if args.decrypt:
        try:
            with open(encrypted_txt, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Input file not found at: {encrypted_txt}")
            return

        decrypted_text = caesar_cipher(text, shift, mode='decrypt')

        print(f"Decrypted text from {encrypted_txt} using key from {key_txt}: \n")
        print(decrypted_text)

    # encrypt
    else:
        try:
            with open(input_txt, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Input file not found at: {input_txt}")
            return

        encrypted_text = caesar_cipher(text, shift, mode='encrypt')

        with open(encrypted_txt, 'w', encoding='utf-8') as file:
            file.write(encrypted_text)

        print(f"Encrypted text from {input_txt} using key from {key_txt}: \n")
        print(encrypted_text)

        print(f"\nResult saved at {encrypted_txt}")
        print("To verify run program with -d flag")


if __name__ == "__main__":
    main()
