import os
import random
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import ALPHABET, KEY_CHARSET, ENCRYPTED_FILE, KEY_FILE, DECRYPTED_CHECK_FILE


def generate_key() -> str:
    """
    Генерирует случайный ключ шифрования длиной 33 символа.
    Символы берутся из набора псевдографики без повторений.
    """
    charset_list: list[str] = list(KEY_CHARSET)
    random.shuffle(charset_list)
    return ''.join(charset_list[:33])


def validate_key(key: str) -> bool:
    """
    Проверяет, что ключ имеет правильную длину (33 символа).
    Допускаются любые символы, включая повторы (но лучше уникальные).
    """
    return len(key) == len(ALPHABET)


def encrypt(text: str, key: str) -> str:
    """
    Шифрует текст методом моноалфавитной замены.
    Русские буквы приводятся к заглавным, символы не из алфавита остаются без изменений.
    
    """
    trans: dict[int, int] = str.maketrans(ALPHABET, key)
    result: list[str] = []
    for ch in text:
        if 'а' <= ch <= 'я' or ch == 'ё':
            if ch == 'ё':
                upper_ch: str = 'Е'
            else:
                upper_ch = chr(ord(ch) - 32)
        elif 'А' <= ch <= 'Я':
            upper_ch = ch
        else:
            upper_ch = ch

        if upper_ch in ALPHABET:
            result.append(chr(trans.get(ord(upper_ch), ord(upper_ch))))
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Расшифровывает текст, используя ключ (обратная подстановка).
    Предполагается, что символы ключа не пересекаются со знаками препинания и латиницей. 
    """
    reverse_trans: dict[int, int] = str.maketrans(key, ALPHABET)
    result: list[str] = []
    for ch in ciphertext:
        if ch in key:
            result.append(chr(reverse_trans.get(ord(ch), ord(ch))))
        else:
            result.append(ch)
    return ''.join(result)


def main() -> None:
    """Основная функция: организует ввод исходного текста, выбор ключа, шифрование и сохранение результатов."""
   
    original_path: str = 'input.txt'
    if not os.path.exists(original_path):
        print(f"Ошибка: {original_path} не найден. Создайте файл с исходным текстом.")
        sys.exit(1)

    with open(original_path, 'r', encoding='utf-8') as f:
        plaintext: str = f.read()

    print("Выберите источник ключа:")
    print("1. Сгенерировать случайный ключ (из символов псевдографики)")
    print("2. Ввести ключ вручную (33 любых символа, лучше уникальных)")
    choice: str = input("Введите 1 или 2: ").strip()

    if choice == '1':
        key: str = generate_key()
        print(f"Сгенерированный ключ: {key}")
    elif choice == '2':
        key = input("Введите ключ (ровно 33 символа, можно любые): ").strip()
        if not validate_key(key):
            print("Неверный ключ. Ключ должен содержать ровно 33 символа.")
            sys.exit(1)
    else:
        print("Неверный выбор.")
        sys.exit(1)

    ciphertext: str = encrypt(plaintext, key)

    with open(ENCRYPTED_FILE, 'w', encoding='utf-8') as f:
        f.write(ciphertext)

    with open(KEY_FILE, 'w', encoding='utf-8') as f:
        f.write(key)

    print("Шифрование выполнено успешно.")
    print(f"Зашифрованный текст сохранён в: encrypted.txt")
    print(f"Ключ сохранён в: key.txt")

    decrypted: str = decrypt(ciphertext, key)
    with open(DECRYPTED_CHECK_FILE, 'w', encoding='utf-8') as f:
        f.write(decrypted)
    print("Проверочная расшифровка сохранена в: decrypted_check.txt")
    print("Сравните её с исходным текстом (учитывайте, что буквы приведены к заглавным, а 'ё' заменена на 'Е').")


if __name__ == '__main__':
    main()