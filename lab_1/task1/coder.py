import random
import os
from typing import Dict, List


def load_cipher_dictionary(dict_path: str) -> Dict[str, List[str]]:
    """Функция для загрузки словаря для шифрования из файла
    на вход принимает путь к файлу словаря
    """
    cipher_dict = {}
    
    with open(dict_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            if '-' not in line:
                continue
            
            left, right = line.split('-', 1)
            
            original = parse_original_char(left.strip())
            replacements = parse_replacements(right.strip())
            
            if replacements:
                cipher_dict[original] = replacements
    
    return cipher_dict


def parse_original_char(left_part: str) -> str:
    """Функция для парсинга исходного символа из левой части строки словаря
    на вход принимает левую часть строки словаря
    возвращает исходный символ (пробел, если левая часть пустая)
    """
    return ' ' if left_part == '' else left_part


def parse_replacements(right_part: str) -> List[str]:
    """Функция для парсинга списка замен из правой части строки словаря
    на вход принимает правую часть строки словаря
    возвращает список символов для замены
    """
    return [r for r in right_part.split() if r != '-']


def encrypt_text(text: str, cipher_dict: Dict[str, List[str]]) -> str:
    """Функция для шифрования переданного текста
    на вход принимает исходный текст и словарь для шифрования
    возвращает зашифрованный текст
    """
    encrypted_chars = []
    for char in text:
        if char in cipher_dict:
            encrypted_chars.append(random.choice(cipher_dict[char]))
        else:
            encrypted_chars.append(char)
    return ''.join(encrypted_chars)


def load_text_from_file(input_path: str) -> str:
    """Функция для загрузки текста из файла
    на вход принимает путь к файлу с исходным текстом
    """
    with open(input_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()
    
    return content


def save_encrypted_text(encrypted_text: str, output_path: str) -> None:
    """Функция для сохранения зашифрованного текста в файл
    на вход принимает зашифрованный текст и путь для сохранения
    """
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(encrypted_text)


def encrypt_file(input_path: str, cipher_dict: Dict[str, List[str]], 
                 output_path: str = 'encrypted_text.txt') -> str:
    """Функция для шифрования текста из файла и сохранения результата
    на вход принимает путь к файлу с исходным текстом, словарь для шифрования 
    и путь для сохранения зашифрованного текста
    возвращает зашифрованный текст
    """
    content = load_text_from_file(input_path)
    encrypted_text = encrypt_text(content, cipher_dict)
    save_encrypted_text(encrypted_text, output_path)
    
    return encrypted_text


def main() -> None:
    """Основная функция для запуска процесса шифрования"""
    os.chdir('task1')
    
    # Загрузка словаря для шифрования
    cipher_dict = load_cipher_dictionary('unicode_dictionary_edited.txt')
    
    # Шифрование файла
    encrypted_text = encrypt_file('text.txt', cipher_dict)
    
    print("Зашифрованный текст:")
    print(encrypted_text)


if __name__ == "__main__":
    main()