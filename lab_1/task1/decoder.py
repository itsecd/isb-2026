import random
from collections import defaultdict
import os


def load_cipher_dictionary(dict_path: str) -> dict:
    """Функция для загрузки словаря для шифрования из файла
    на вход принимает путь к файлу словаря
    """
    cipher_dict = {}
    
    with open(dict_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            line = line.strip()
            if '-' in line:
                left, right = line.split('-', 1)
                
                left = left.strip()
                if left == '':
                    original = ' '
                else:
                    original = left
                
                replacements = [r for r in right.strip().split() if r and r != '-']
                
                if replacements:
                    cipher_dict[original] = replacements
    
    return cipher_dict


def create_decipher_dictionary(cipher_dict: dict) -> dict:
    """Функция для создания обратного словаря для расшифровки
    на вход принимает словарь для шифрования
    """
    decipher_dict = {}
    
    for original, replacements in cipher_dict.items():
        for replacement in replacements:
            decipher_dict[replacement] = original
    
    return decipher_dict


def load_encrypted_text(file_path: str) -> str:
    """Функция для загрузки зашифрованного текста из файла
    на вход принимает путь к файлу с зашифрованным текстом
    """
    with open(file_path, 'r', encoding='utf-8') as encrypted_file:
        encrypted_content = encrypted_file.read()
    
    return encrypted_content


def decrypt_text(encrypted_content: str, decipher_dict: dict) -> str:
    """Функция для расшифровки текста
    на вход принимает зашифрованный текст и словарь для расшифровки
    """
    decrypted_text = ""
    
    for char in encrypted_content:
        if char in decipher_dict:
            decrypted_text += decipher_dict[char]
        else:
            decrypted_text += char
    
    return decrypted_text


def save_decrypted_text(decrypted_text: str, output_path: str) -> None:
    """Функция для сохранения расшифрованного текста в файл
    на вход принимает расшифрованный текст и путь для сохранения
    """
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(decrypted_text)
    
    print(f"Расшифрованный текст сохранен в файл '{output_path}'")


def compare_with_original(original_path: str, decrypted_text: str) -> bool:
    """Функция для сравнения расшифрованного текста с оригиналом
    на вход принимает путь к оригинальному файлу и расшифрованный текст
    возвращает True если тексты совпадают, иначе False
    """
    try:
        with open(original_path, 'r', encoding='utf-8') as original_file:
            original_text = original_file.read()
        
        return original_text == decrypted_text
    except FileNotFoundError:
        return None


def main() -> None:
    """Основная функция для запуска процесса расшифровки"""
    os.chdir('task1')
    
    # Загрузка словаря для шифрования
    cipher_dict = load_cipher_dictionary('unicode_dictionary_edited.txt')
    
    # Создание обратного словаря для расшифровки
    decipher_dict = create_decipher_dictionary(cipher_dict)
    
    # Чтение зашифрованного текста
    encrypted_content = load_encrypted_text('encrypted_text.txt')
    
    # Расшифровка текста
    decrypted_text = decrypt_text(encrypted_content, decipher_dict)
    
    print("\nРасшифрованный текст:")
    print(decrypted_text)
    
    # Сохранение расшифрованного текста в файл
    save_decrypted_text(decrypted_text, 'decrypted_text.txt')
    
    # Дополнительная проверка: сравниваем с оригиналом (если есть)
    comparison_result = compare_with_original('text.txt', decrypted_text)
    
    if comparison_result is True:
        print("\nУСПЕХ: Расшифрованный текст полностью совпадает с оригиналом!")
    elif comparison_result is False:
        print("\nОШИБКА: Расшифрованный текст НЕ совпадает с оригиналом")
    else:
        print("\nФайл text.txt не найден для сравнения")


if __name__ == "__main__":
    main()