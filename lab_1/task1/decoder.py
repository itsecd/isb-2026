import os
from typing import Dict, List


def read_dictionary_file(dict_path: str) -> List[str]:
    """Чтение строк словаря из файла"""
    with open(dict_path, 'r', encoding='utf-8') as dict_file:
        return dict_file.readlines()


def parse_cipher_dictionary(lines: List[str]) -> Dict[str, List[str]]:
    """Парсинг словаря шифрования из списка строк"""
    cipher_dict = {}

    for line in lines:
        line = line.strip()

        if '-' not in line:
            continue

        left, right = line.split('-', 1)

        left = left.strip()
        original = ' ' if left == '' else left

        replacements = [r for r in right.strip().split() if r and r != '-']

        if replacements:
            cipher_dict[original] = replacements

    return cipher_dict


def load_cipher_dictionary(dict_path: str) -> Dict[str, List[str]]:
    """Загрузка словаря шифрования из файла"""
    lines = read_dictionary_file(dict_path)
    return parse_cipher_dictionary(lines)


def create_decipher_dictionary(cipher_dict: Dict[str, List[str]]) -> Dict[str, str]:
    """Создание обратного словаря для расшифровки"""
    decipher_dict = {}

    for original, replacements in cipher_dict.items():
        for replacement in replacements:
            decipher_dict[replacement] = original

    return decipher_dict


def load_encrypted_text(file_path: str) -> str:
    """Загрузка зашифрованного текста из файла"""
    with open(file_path, 'r', encoding='utf-8') as encrypted_file:
        return encrypted_file.read()


def decrypt_text(encrypted_content: str, decipher_dict: Dict[str, str]) -> str:
    """Расшифровка текста"""
    decrypted_chars = []

    for char in encrypted_content:
        if char in decipher_dict:
            decrypted_chars.append(decipher_dict[char])
        else:
            decrypted_chars.append(char)

    return ''.join(decrypted_chars)


def save_decrypted_text(decrypted_text: str, output_path: str) -> None:
    """Сохранение расшифрованного текста в файл"""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(decrypted_text)

    print(f"Расшифрованный текст сохранен в файл '{output_path}'")


def compare_with_original(original_path: str, decrypted_text: str):
    """Сравнение расшифрованного текста с оригиналом"""
    try:
        with open(original_path, 'r', encoding='utf-8') as original_file:
            original_text = original_file.read()

        return original_text == decrypted_text

    except FileNotFoundError:
        return None


def main() -> None:
    """Основная функция для запуска процесса расшифровки"""
    os.chdir('task1')

    cipher_dict = load_cipher_dictionary('unicode_dictionary_edited.txt')
    decipher_dict = create_decipher_dictionary(cipher_dict)

    encrypted_content = load_encrypted_text('encrypted_text.txt')
    decrypted_text = decrypt_text(encrypted_content, decipher_dict)

    print("\nРасшифрованный текст:")
    print(decrypted_text)

    save_decrypted_text(decrypted_text, 'decrypted_text.txt')

    comparison_result = compare_with_original('text.txt', decrypted_text)

    if comparison_result is True:
        print("\nУСПЕХ: Расшифрованный текст полностью совпадает с оригиналом!")
    elif comparison_result is False:
        print("\nОШИБКА: Расшифрованный текст НЕ совпадает с оригиналом")
    else:
        print("\nФайл text.txt не найден для сравнения")


if __name__ == "__main__":
    main()