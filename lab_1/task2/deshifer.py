#По идее сначала был код, который считал количевтво повторений каждого символа в закоденном файле и сравнивал с повтряемостью, формируя первоначальный декодлирующий словарь. Но с задаччей справлялся он откровенно плохо, так что пришлось больше половины ключа исправлять ручками.

import os
import json
from typing import Dict


def load_encrypted_text(file_path: str) -> str:
    """Функция для загрузки зашифрованного текста из файла
    на вход принимает путь к файлу с зашифрованным текстом
    возвращает содержимое файла в виде строки
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        encrypted_text = file.read()
    return encrypted_text


def load_cipher_key(key_path: str) -> Dict[str, str]:
    """Функция для загрузки ключа шифрования из JSON файла
    на вход принимает путь к файлу с ключом
    возвращает словарь соответствия зашифрованных символов русским буквам
    в случае отсутствия файла программа завершается
    """
    try:
        with open(key_path, 'r', encoding='utf-8') as f:
            cipher_to_russian = json.load(f)
        print("Ключ загружен из cipher_key.json")
        return cipher_to_russian
    except FileNotFoundError:
        print("Ошибка: файл cipher_key.json не найден!")
        exit(1)


def decrypt_text(encrypted_text: str, cipher_key: Dict[str, str]) -> str:
    """Функция для расшифровки текста с использованием ключа
    на вход принимает зашифрованный текст и словарь соответствия символов
    возвращает расшифрованный текст
    """
    decrypted = ""
    for char in encrypted_text:
        if char in cipher_key:
            decrypted += cipher_key[char]
        else:
            decrypted += char
    return decrypted


def save_decrypted_text(decrypted_text: str, output_path: str) -> None:
    """Функция для сохранения расшифрованного текста в файл
    на вход принимает расшифрованный текст и путь для сохранения
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)


def print_results_summary() -> None:
    """Функция для вывода итоговой информации о результате работы"""
    print("\n" + "=" * 50)
    print("Результат сохранен в decoded.txt")
    print("=" * 50)


def main() -> None:
    """Основная функция для запуска процесса расшифровки
    использует предварительно созданный ключ шифрования
    """
    os.chdir('task2')
    
    # Загрузка зашифрованного текста
    encrypted_text = load_encrypted_text('shifred_text.txt')
    
    # Загрузка ключа шифрования
    cipher_key = load_cipher_key('cipher_key.json')
    
    # Расшифровка текста
    decrypted_text = decrypt_text(encrypted_text, cipher_key)
    
    # Вывод расшифрованного текста
    print(decrypted_text)
    
    # Сохранение результата
    save_decrypted_text(decrypted_text, 'decoded.txt')
    
    # Вывод итоговой информации
    print_results_summary()


if __name__ == "__main__":
    main()