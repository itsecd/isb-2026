from Ru import ALPHABET
from key import encrypt_key


def normalize_text(text):
    """Приводит текст к формату, указанному в задании"""
    return text.upper().replace("Ё", "Е")


def encrypt_text(text, encrypt_key_dict):
    """Шифрует текст с помощью словаря замены"""
    result = ""

    for char in text:
        if char in encrypt_key_dict:
            result += encrypt_key_dict[char]
        else:
            result += char

    return result


def save_key(key_dict, filename):
    """Сохраняет ключ шифрования в файл"""
    with open(filename, "w", encoding="utf-8") as f:
        for char in ALPHABET:
            f.write(f"{char} : {key_dict[char]}\n")


def main():
    with open("text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    text = normalize_text(text)
    encrypted_text = encrypt_text(text, encrypt_key)

    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_text)

    save_key(encrypt_key, "encrypt_key.txt")


if __name__ == "__main__":
    main()
