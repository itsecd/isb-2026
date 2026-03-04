from constants import ALPHABET, INPUT_FILE, KEY_FILE, DECODED_FILE, CODED_FILE


def read_file(filename: str) -> str:
    """
    Читает содержимое файла и возвращает его в виде строки
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename: str, text: str):
    """Записывает текст в файл"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def clean_key(key: str) -> str:
    """Очищает ключ от символов, не входящих в алфавит"""
    return "".join(char.lower() for char in key if char.lower() in ALPHABET)


def generate_key(text: str, key: str) -> str:
    """Продолжает ключ повторяя его до длины текста"""
    key_extended = ""
    key_index = 0

    for char in text:
        if char.lower() in ALPHABET:
            key_extended += key[key_index % len(key)]
            key_index += 1
        else:
            key_extended += char

    return key_extended


def encrypt(text: str, key: str) -> str:
    """Шифрует текст"""
    key_extended = generate_key(text, key)
    result = ""

    for i in range(len(text)):
        char = text[i]

        if char.lower() in ALPHABET:
            text_index = ALPHABET.index(char.lower())
            key_index = ALPHABET.index(key_extended[i])
            new_index = (text_index + key_index) % len(ALPHABET)
            new_char = ALPHABET[new_index]

            if char.isupper():
                result += new_char.upper()
            else:
                result += new_char
        else:
            result += char

    return result


def decrypt(text: str, key: str) -> str:
    """Расшифровывает"""
    key_extended = generate_key(text, key)
    result = ""

    for i in range(len(text)):
        char = text[i]

        if char.lower() in ALPHABET:
            text_index = ALPHABET.index(char.lower())
            key_index = ALPHABET.index(key_extended[i])
            new_index = (text_index - key_index) % len(ALPHABET)
            new_char = ALPHABET[new_index]

            if char.isupper():
                result += new_char.upper()
            else:
                result += new_char
        else:
            result += char

    return result


def main():
    text = read_file(INPUT_FILE)
    key = clean_key(read_file(KEY_FILE))

    if not key:
        print("Key error.")
        return


    coded_text = encrypt(text, key)
    write_file(CODED_FILE, coded_text)


    coded_from_file = read_file(CODED_FILE)
    decoded_text = decrypt(coded_from_file, key)
    write_file(DECODED_FILE, decoded_text)

    original_text = read_file(INPUT_FILE)
    decoded_text_check = read_file(DECODED_FILE)

    if original_text == decoded_text_check:
        print("success ^-^")
    else:
        print("oh no, the texts don't match T-T")


if __name__ == "__main__":
    main()
