# -*- coding: utf-8 -*-
import os
from pathlib import Path
from files1 import INPUT_FILE, KEY_FILE, ENCRYPTED_FILE, CHECK_FILE

ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

def read_key_from_file(key_filepath):
    """Чтение ключа из файла"""
    try:
        with open(key_filepath, 'r', encoding='utf-8') as f:
            key = f.read().strip()
            return key
    except FileNotFoundError:
        raise FileNotFoundError(f"Ошибка: файл {key_filepath} не найден")
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {key_filepath}: {e}")

def read_text_from_file(filepath):
    """Чтение текста из файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            if not text:
                raise ValueError(f"Файл {filepath} пуст")
            return text.upper()
    except FileNotFoundError:
        raise FileNotFoundError(f"Ошибка: файл {filepath} не найден")
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filepath}: {e}")

def write_text_to_file(filepath, content):
    """Запись текста в файл"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Ошибка при записи файла {filepath}: {e}")

def encrypt_vigenere(text, key, alphabet):
    """Шифрование текста методом Виженера"""
    try:
        key_indices = [alphabet.index(k) for k in key]
    except ValueError as e:
        raise ValueError(f"Ошибка: символ в ключе не найден в алфавите - {e}")
    
    result = []
    for i, char in enumerate(text):
        if char in alphabet:
            char_index = alphabet.index(char)
            key_index = key_indices[i % len(key)]
            result.append(alphabet[(char_index + key_index) % len(alphabet)])
        else:
            result.append(char)
    
    return ''.join(result)

def decrypt_vigenere(encrypted_text, key, alphabet):
    """Расшифровка текста методом Виженера"""
    try:
        key_indices = [alphabet.index(k) for k in key]
    except ValueError as e:
        raise ValueError(f"Ошибка: символ в ключе не найден в алфавите - {e}")
    
    result = []
    for i, char in enumerate(encrypted_text):
        if char in alphabet:
            char_index = alphabet.index(char)
            key_index = key_indices[i % len(key)]
            result.append(alphabet[(char_index - key_index) % len(alphabet)])
        else:
            result.append(char)
    
    return ''.join(result)

def main():
    """Основная функция для шифрования и расшифровки текста методом Виженера"""
    try:
    
        key = read_key_from_file(KEY_FILE)
        
        text = read_text_from_file(INPUT_FILE)
        
        encrypted_text = encrypt_vigenere(text, key, ALPHABET)
        
        write_text_to_file(ENCRYPTED_FILE, encrypted_text)
        
        decrypted_text = decrypt_vigenere(encrypted_text, key, ALPHABET)
        
        write_text_to_file(CHECK_FILE, decrypted_text)
        
        print("Созданы файлы: encrypted.txt, check.txt")
        print(f"Исходный текст прочитан из файла: {INPUT_FILE}")
        
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Ошибка: {e}")
        return

if __name__ == '__main__':
    main()
