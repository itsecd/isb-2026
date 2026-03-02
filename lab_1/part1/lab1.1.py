ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def read_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename: str, text: str):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def clean_key(key: str) -> str:
    return "".join(char.lower() for char in key if char.lower() in ALPHABET)


def generate_key(text: str, key: str) -> str:
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
    text = read_file("input.txt")
    key = clean_key(read_file("key.txt"))

    if not key:
        print("Key error.")
        return


    coded_text = encrypt(text, key)
    write_file("coded.txt", coded_text)


    coded_from_file = read_file("coded.txt")
    decoded_text = decrypt(coded_from_file, key)
    write_file("decoded.txt", decoded_text)

    original_text = read_file("input.txt")
    decoded_text_check = read_file("decoded.txt")

    if original_text == decoded_text_check:
        print("success ^-^")
    else:
        print("oh no, the texts don't match T-T")


if __name__ == "__main__":
    main()
