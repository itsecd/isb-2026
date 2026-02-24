import argparse
from alphabet.py import ALPHABET

def parse_args():
    """
    Функция для парсинга аргументов командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Путь к файлу с исходным текстом")
    parser.add_argument("-o", "--output", type=str, required=True, help="Путь для записи файла с зашифрованным текстом")
    parser.add_argument("-k", "--key", type=str, required=True, help="Путь до файла с ключом")
    args = parser.parse_args()
    return args.input, args.output, args.key


def format_str(input_str: str, alphabet: str) -> str:
    """
    Функция, которая оставляет ну типо короче от ключа только буковки.
    """
    result_str = ""
    for character in input_str:
        if character.lower() in alphabet:
            result_str += character
    return result_str


def encrypt_character(input_chr: str, key: str, alphabet: str, alphabet_dict: dict) -> str:
    """
    Функция для шифровки одного символа.
    """
    lenght = len(alphabet_dict)
    return alphabet[((alphabet_dict[input_chr])+(alphabet_dict[key]))%lenght]


def encrypt_text(input_str: str, key: str, alphabet: str, alphabet_dict: dict):
    """
    Фунция для шифровки всего текста.
    """
    result_str = ""
    key_pointer = 0
    for character in input_str:
        if character in alphabet:
            result_str += encrypt_character(character,key[key_pointer], alphabet, alphabet_dict)
            if (key_pointer == len(key)-1):
                key_pointer = 0
            else:
                key_pointer += 1
        else:
            result_str += character
    return result_str


def decrypt_character(input_chr: str, key: str, alphabet: str, alphabet_dict: dict) -> str:
    """
    Функция для расшифровки одного символа.
    """
    lenght = len(alphabet_dict)
    return alphabet[(lenght+(alphabet_dict[input_chr])-(alphabet_dict[key]))%lenght]


def decrypt_text(input_str: str, key: str, alphabet: str, alphabet_dict: dict):
    """
    Функция для расшифровки всего текста.
    """
    result_str = ""
    key_pointer = 0
    for character in input_str:
        if character in alphabet:
            result_str += decrypt_character(character, key[key_pointer], alphabet, alphabet_dict)
            if (key_pointer == len(key)-1):
                key_pointer = 0
            else:
                key_pointer += 1
        else:
            result_str += character
    return result_str


def main():
    """
    Это мэйн. !!!ИНВАЛИДНАЯ КОЛЯСКА ALERET!!! Зато без вайбкодинга, только шизокод
    """
    alphabet_dict = dict.fromkeys(ALPHABET, 0)
    j=0
    for i in alphabet:
        alphabet_dict[i] += j
        j += 1
    
    input_path, output_path, key_path = parse_args()
    with open(key_path, "r", encoding="utf-8") as key_file:
        key = format_str(key_file.read(), ALPHABET)
    with open (input_path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    cipher_text = encrypt_text(text, key, ALPHABET, alphabet_dict)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(cipher_text)
    print(decrypt_text(cipher_text, key, ALPHABET, alphabet_dict))


if __name__ == "__main__":
    main()


