import argparse

def ReadFile(filename: str) -> None:
    """
    Reading text from a file. 
    """
    with open(filename, "r", encoding = "utf-8") as file:
        text = file.read()

    return text


ALPHABET_LOWERCASE = tuple('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
ALPHABET_UPPERCASE = tuple('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
KEY = (15, 16, 3, 16, 12, 21, 11, 2, 29, 26, 6, 3, 19, 12)


def TrithemiusCipher(original_text) -> tuple[str]:
    """ 
    Text encryption using a trithemius cipher.
    """
    alphabet = None
    encrypted_text = []
    key = 0
    
    for letter in original_text:
        if not letter.isalpha():
            encrypted_text.append(letter)
            continue

        alphabet = ALPHABET_LOWERCASE if letter.islower() else ALPHABET_UPPERCASE
        letter_index = alphabet.index(letter)
        new_letter_index = (letter_index + KEY[key]) % len(alphabet)
        letter = alphabet[new_letter_index]
        encrypted_text.append(letter)
        key = (key + 1) % len(KEY)
    
    return encrypted_text


def WriteFile(text: tuple[str], filename: str) -> None:
    """ 
    Writing to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for word in text:
            file.write(word)


def DecryptionTrithemiusCipher(encrypted_text: tuple[str]) -> tuple[str]:
    """ 
    Text decryption using a trithemius cipher.
    """
    alphabet = None
    decrypted_text = []
    key = 0
    
    for letter in encrypted_text:
        if not letter.isalpha():
            decrypted_text.append(letter)
            continue

        alphabet = ALPHABET_LOWERCASE if letter.islower() else ALPHABET_UPPERCASE
        letter_index = alphabet.index(letter)
        new_letter_index = (letter_index - KEY[key]) % len(alphabet)
        letter = alphabet[new_letter_index]
        decrypted_text.append(letter)
        key = (key + 1) % len(KEY)
    
    return decrypted_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--original_text', '-o', type=str, help="Path to the file with the original text")
    parser.add_argument('--encrypted_text', '-e', type=str, help="Path to the file with the encrypted text")
    args = parser.parse_args()

    if args.original_text is None:
        args.original_text = "non_encrypted_text_task_1.txt"
    if args.encrypted_text is None:
        args.encrypted_text = "task_1_result.txt"

    try:
        original_text = ReadFile(args.original_text)
        encrypted_text = TrithemiusCipher(original_text)
        WriteFile(encrypted_text, args.encrypted_text)
        decrypted_text = DecryptionTrithemiusCipher(encrypted_text)
        decrypted_text.extend(["\n\nключ - НОВОКУЙБЫШЕВСК"])
        WriteFile(decrypted_text, "check_task_1_result.txt")

    except FileNotFoundError:
        print("Error: file not found")


if __name__ == "__main__":

    main()

