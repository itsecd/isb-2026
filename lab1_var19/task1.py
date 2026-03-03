import os
import argparse
from typing import Dict

from constants import (
    RUSSIAN_ALPHABET, ALPHABET_LENGTH,
    TASK1_ENCRYPTED_FILE, TASK1_KEY_FILE, TASK1_ORIGINAL_FILE,
)


def caesar_encrypt(text: str, shift: int) -> str:
    """
    Шифрует текст шифром Цезаря с заданным сдвигом.
    
    Args:
        text: Исходный текст для шифрования
        shift: Величина сдвига (положительное число)
    
    Returns:
        str: Зашифрованный текст
    
    Raises:
        ValueError: Если текст содержит символы, отсутствующие в алфавите
    """
    result = []
    
    for char in text:
        upper_char = char.upper()
        
        if upper_char in RUSSIAN_ALPHABET:
            idx = RUSSIAN_ALPHABET.index(upper_char)
            new_idx = (idx + shift) % ALPHABET_LENGTH
            encrypted_char = RUSSIAN_ALPHABET[new_idx]
            
            if char.islower():
                encrypted_char = encrypted_char.lower()
            
            result.append(encrypted_char)
        
        else:
            #Символы не из алфавита не меняем
            result.append(char)
    
    return "".join(result)


def caesar_decrypt(encrypted_text: str, shift: int) -> str:
    """
    Дешифрует текст, зашифрованный шифром Цезаря.
    
    Args:
        encrypted_text: Зашифрованный текст
        shift: Величина сдвига, использованная при шифровании
    
    Returns:
        str: Расшифрованный текст
    """
    return caesar_encrypt(encrypted_text, -shift)


def shift_to_key(shift: int) -> Dict[str, str]:
    """
    Преобразует сдвиг в формат ключа подстановки.
    
    Args:
        shift: Величина сдвига
    
    Returns:
        Dict[str, str]: Ключ подстановки (словарь: исходная буква -> замена)
    """
    key = {}
    for i, char in enumerate(RUSSIAN_ALPHABET):
        new_idx = (i + shift) % ALPHABET_LENGTH
        key[char] = RUSSIAN_ALPHABET[new_idx]
    return key


def save_shift(shift: int, filename: str) -> None:
    """
    Сохраняет сдвиг в файл.
    
    Args:
        shift: Величина сдвига
        filename: Имя файла для сохранения
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"shift:{shift}\n")
        f.write("Подстановка (исходная -> замена):\n")
        for i, char in enumerate(RUSSIAN_ALPHABET):
            new_idx = (i + shift) % ALPHABET_LENGTH
            f.write(f"{char}:{RUSSIAN_ALPHABET[new_idx]}\n")


def ensure_directories() -> None:
    """Создает необходимые директории, если их нет."""

    os.makedirs("task1", exist_ok=True)


def read_text_file(filename: str) -> str:
    """
    Читает текст из файла.
    
    Args:
        filename: Имя файла
    
    Returns:
        str: Содержимое файла
    """
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(filename: str, content: str) -> None:
    """
    Записывает текст в файл.
    
    Args:
        filename: Имя файла
        content: Содержимое для записи
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def task1_encrypt(shift: int) -> int:
    """
    Шифрует текст шифром Цезаря.
    
    Args:
        shift: Величина сдвига для шифрования
    
    Returns:
        int: Сдвиг, использованный при шифровании
    """
    
    original_text = read_text_file(TASK1_ORIGINAL_FILE)
    print(f"Исходный текст прочитан, длина: {len(original_text)} символов")
    print(f"Используется сдвиг: {shift}")
    
    encrypted_text = caesar_encrypt(original_text, shift)
    
    write_text_file(TASK1_ENCRYPTED_FILE, encrypted_text)
    save_shift(shift, TASK1_KEY_FILE)
    
    decrypted_text = caesar_decrypt(encrypted_text, shift)
    write_text_file("task1/decrypted.txt", decrypted_text)
    
    print(f"Зашифрованный текст сохранен в: {TASK1_ENCRYPTED_FILE}")
    print(f"Ключ сохранен в: {TASK1_KEY_FILE}")
    
    if decrypted_text == original_text:
        print("Проверка дешифровки: успешно")
    else:
        print("Проверка дешифровки: ошибка")
    
    return shift


def parse_arguments() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.
    
    Returns:
        argparse.Namespace: Объект с аргументами
    """
    parser = argparse.ArgumentParser(
        description="Шифрование текста шифром Цезаря",
        epilog="""
Примеры использования:
  python main.py --shift 3
  python main.py -s 7
  python main.py --help
        """
    )
    
    parser.add_argument(
        '-s', '--shift',
        type=int,
        default=1,
        help='Величина сдвига для шифра Цезаря (по умолчанию: 1)'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        default=TASK1_ORIGINAL_FILE,
        help=f'Путь к исходному файлу (по умолчанию: {TASK1_ORIGINAL_FILE})'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=TASK1_ENCRYPTED_FILE,
        help=f'Путь для сохранения зашифрованного файла (по умолчанию: {TASK1_ENCRYPTED_FILE})'
    )
    
    parser.add_argument(
        '--key',
        type=str,
        default=TASK1_KEY_FILE,
        help=f'Путь для сохранения ключа (по умолчанию: {TASK1_KEY_FILE})'
    )
    
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    
    print("Задание 1")
    print("Шифр Цезаря (моноалфавитная подстановка со сдвигом)\n")
    
    global TASK1_ORIGINAL_FILE, TASK1_ENCRYPTED_FILE, TASK1_KEY_FILE
    
    if args.input != TASK1_ORIGINAL_FILE:
        TASK1_ORIGINAL_FILE = args.input
    if args.output != TASK1_ENCRYPTED_FILE:
        TASK1_ENCRYPTED_FILE = args.output
    if args.key != TASK1_KEY_FILE:
        TASK1_KEY_FILE = args.key
    
    ensure_directories()
    
    alphabet_length = len(RUSSIAN_ALPHABET)
    if args.shift < 0:
        print(f"Предупреждение: отрицательный сдвиг {args.shift} будет преобразован в положительный")
        args.shift = args.shift % alphabet_length
    
    if args.shift >= alphabet_length:
        print(f"Предупреждение: сдвиг {args.shift} больше длины алфавита ({alphabet_length})")
        print(f"Будет использован сдвиг: {args.shift % alphabet_length}")
        args.shift = args.shift % alphabet_length
    
    task1_encrypt(args.shift)
    
    print(f"\nРезультаты сохранены в директории task1\n")


if __name__ == "__main__":
    main()