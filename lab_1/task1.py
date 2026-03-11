"""
Задание 1: Шифрование текста шифром Цезаря
Лабораторная работа №1, Вариант №21

Текст загружается из файла task1_original.txt
"""

import os
from caesar_cipher import CaesarCipher
from frequency_analyzer import FrequencyAnalyzer


# Папка для результатов
RESULTS_DIR = 'results'


def ensure_results_dir():
    """Создает папку для результатов."""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)


def load_original_text(filename: str = 'task1_original.txt') -> str:
    """
    Загружает исходный текст из файла.
    
    Args:
        filename (str): Имя файла с исходным текстом
        
    Returns:
        str: Исходный текст
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f" ОШИБКА: Файл {filename} не найден!")
        print("Создайте файл с исходным текстом.")
        return ""


def write_file(path: str, text: str) -> None:
    """Записывает текст в файл."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def run_task1():
    """
    Выполнение задания 1: Шифрование собственного текста
    """
    print("=" * 70)
    print("ЗАДАНИЕ 1: Шифрование текста шифром Цезаря")
    print("=" * 70)
    
    # Загрузка исходного текста из файла
    print("\n1. ЗАГРУЗКА ИСХОДНОГО ТЕКСТА:")
    print("-" * 70)
    original_text = load_original_text('task1_original.txt')
    
    if not original_text:
        print(" Ошибка загрузки текста!")
        return None, None
    
    print(f"Длина текста: {len(original_text)} символов")
    print(f"\nТекст (первые 500 символов):")
    print(original_text[:500] + "..." if len(original_text) > 500 else original_text)
    
    # Инициализация
    cipher = CaesarCipher(shift=5)  # Ключ шифрования = 5
    analyzer = FrequencyAnalyzer()
    
    # Шифрование
    print(f"\n2. ШИФРОВАНИЕ (ключ={cipher.get_shift()}):")
    print("-" * 70)
    encrypted_text = cipher.encrypt(original_text)
    print(encrypted_text[:500] + "..." if len(encrypted_text) > 500 else encrypted_text)
    
    # Расшифрование для проверки
    print(f"\n3. РАСШИФРОВАНИЕ (для проверки):")
    print("-" * 70)
    decrypted_text = cipher.decrypt(encrypted_text)
    print(decrypted_text[:500] + "..." if len(decrypted_text) > 500 else decrypted_text)
    
    # Проверка корректности
    if original_text.lower() == decrypted_text.lower():
        print("\n ПРОВЕРКА: Расшифрованный текст совпадает с исходным!")
    else:
        print("\n ПРОВЕРКА: Ошибка расшифрования!")
    
    # Частотный анализ
    print("\n4. ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА:")
    freq = analyzer.analyze(encrypted_text)
    analyzer.print_frequency_table(freq)
    
    # Сохранение результатов
    ensure_results_dir()
    write_file(f'{RESULTS_DIR}/task1_original.txt', original_text)
    write_file(f'{RESULTS_DIR}/task1_encrypted.txt', encrypted_text)
    write_file(f'{RESULTS_DIR}/task1_key.txt', f"Ключ шифрования (сдвиг): {cipher.get_shift()}\n")
    analyzer.save_frequency_table(freq, f'{RESULTS_DIR}/task1_frequency.txt')
    
    print(f"\n Результаты задания 1 сохранены в папку '{RESULTS_DIR}/'")
    print("\nФайлы:")
    print("  - task1_original.txt")
    print("  - task1_encrypted.txt")
    print("  - task1_key.txt")
    print("  - task1_frequency.txt")
    
    return cipher, analyzer


if __name__ == "__main__":
    run_task1()