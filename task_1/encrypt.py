import os
import sys
import random

INPUT_TEXT_FILE = "Wolf.txt"
ENCRYPTED_FILE = "encrypted.txt"
KEY_FILE = "cipher_key.txt"
RUSSIAN = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def generate_cipher_alphabet() -> str:
    """Создаёт случайную перестановку русского алфавита"""
    letters = list(RUSSIAN)
    random.shuffle(letters)
    return "".join(letters)


def save_key_and_encrypt(input_path: str, encrypted_path: str, key_path: str) -> None:
    if not os.path.exists(input_path):
        print(f"Ошибка: входной файл '{input_path}' не найден")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        text = f.read().lower()

    cipher_alphabet = generate_cipher_alphabet()
    trans_dict = str.maketrans(RUSSIAN, cipher_alphabet)

    key_line = f"{RUSSIAN} → {cipher_alphabet}"
    with open(key_path, "w", encoding="utf-8") as f:
        f.write(key_line)

    encrypted = text.translate(trans_dict)
    with open(encrypted_path, "w", encoding="utf-8") as f:
        f.write(encrypted)

    print("Шифрование выполнено.")
    print(f"Ключ сохранён в: {key_path}")
    print(f"Зашифрованный текст сохранён в: {encrypted_path}")
    print("\nКлюч:")
    print(key_line)


def main() -> None:
    '''
    Зашифровывает входной файл
    Сохраняет результат в выходной файл
    '''
    print("Программа шифрования текста (моноалфавитная замена)\n")
    try:
        save_key_and_encrypt(INPUT_TEXT_FILE, ENCRYPTED_FILE, KEY_FILE)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()