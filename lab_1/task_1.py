import argparse
import sys

def caesar_cipher(text, shift, mode='encrypt'):
    """
    Шифр Цезаря для русского и английского алфавитов
    :param text: Исходный текст, который необходимо зашифровать или дешифровать
    :param shift: Ключ, определяющий величину сдвига символов в алфавите
    :param mode: Режим работы: 'encrypt' для шифрования,'decrypt' для дешифрования
    :return: Строка с примененным сдвигом
    """
    if mode == 'decrypt':
        shift = -shift

    ru_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ru_upper = ru_lower.upper()
    en_lower = "abcdefghijklmnopqrstuvwxyz"
    en_upper = en_lower.upper()

    result = []

    for char in text:
        if char in ru_lower:
            index = (ru_lower.find(char) + shift) % len(ru_lower)
            result.append(ru_lower[index])
        elif char in ru_upper:
            index = (ru_upper.find(char) + shift) % len(ru_upper)
            result.append(ru_upper[index])
        elif char in en_lower:
            index = (en_lower.find(char) + shift) % len(en_lower)
            result.append(en_lower[index])
        elif char in en_upper:
            index = (en_upper.find(char) + shift) % len(en_upper)
            result.append(en_upper[index])
        else:
            result.append(char)

    return "".join(result)

def parse_args() -> argparse.Namespace:
    """
    Разбор аргументов командной строки
    :return: аргументы командной строки
    """

    p = argparse.ArgumentParser()

    p.add_argument("-o",
                   "--original_text_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\original_text_task_1.txt",
                   help="Путь к оригинальному тексту")

    p.add_argument("-k",
                   "--key_value",
                   required=True,
                   help="Ключ для шифра Цезаря")

    p.add_argument("-kp",
                   "--key_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\key_task_1.txt",
                   help="Путь для сохранения значения ключа")

    p.add_argument("-e",
                   "--encrypt_text_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\encrypted_text_task_1.txt",
                   help="Путь для сохранения зашифрованного текста")

    p.add_argument("-d",
                   "--decrypt_text_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\decrypted_text_task_1.txt",
                   help="Путь для сохранения дешифрованного текста")

    return p.parse_args()

def main():
    args = parse_args()

    try:
        with open(args.original_text_path, "r") as f:
            original_text = f.read()
    except FileNotFoundError:
        print(f"File path {args.original_text_path} was not found")
        sys.exit(1)

    encrypted_text = caesar_cipher(original_text, int(args.key_value), mode='encrypt')



if __name__ == "__main__":
    main()