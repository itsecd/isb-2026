"""
Задание 1: Шифрование текста шифром Цезаря
Лабораторная работа №1, Вариант №21
"""

import os
from caesar_cipher import CaesarCipher
from frequency_analyzer import FrequencyAnalyzer


# Создаем папку для результатов
RESULTS_DIR = 'results'
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


def run_task1():
    """
    Выполнение задания 1: Шифрование собственного текста
    """
    print("="*70)
    print("ЗАДАНИЕ 1: Шифрование текста шифром Цезаря")
    print("="*70)
    
    # Инициализация
    cipher = CaesarCipher(shift=5)  # Ключ шифрования = 5
    analyzer = FrequencyAnalyzer()
    
    # Исходный текст (более 500 символов)
    original_text = """
Криптография - это наука о методах обеспечения конфиденциальности, 
целостности данных и аутентификации. Шифр Цезаря является одним из 
простейших методов шифрования, который был известен еще в древнем Риме.
Юлий Цезарь использовал этот шифр для секретной переписки с своими 
полководцами. Принцип работы шифра заключается в замене каждой буквы 
текста на букву, находящуюся на определенное количество позиций левее 
или правее её в алфавите. Несмотря на простоту, шифр Цезаря сыграл 
важную роль в истории криптографии. В современном мире этот метод 
используется преимущественно в образовательных целях для изучения 
основ криптографии. Шифр Цезаря относится к классу шифров подстановки,
где каждый символ открытого текста заменяется другим символом. 
Ключом шифра является величина сдвига. Для русского алфавита 
существует тридцать три возможных сдвига, для английского - 
двадцать шесть. Взлом шифра Цезаря может быть осуществлен методом 
полного перебора всех возможных ключей или с помощью частотного 
анализа. Частотный анализ основан на том факте, что в любом тексте 
некоторые буквы встречаются чаще других. Например, в русском языке 
наиболее часто встречаются буквы О, А, Е, И, Н, Т, С, Р. Зная это, 
можно попытаться определить ключ шифрования, сравнив частоты букв 
в зашифрованном тексте с известными частотами букв в открытом тексте.
"""
    
    print(f"\n1. ИСХОДНЫЙ ТЕКСТ (длина: {len(original_text)} символов):")
    print("-"*70)
    print(original_text)
    
    # Шифрование
    encrypted_text = cipher.encrypt(original_text)
    print(f"\n2. ЗАШИФРОВАННЫЙ ТЕКСТ (ключ={cipher.get_shift()}):")
    print("-"*70)
    print(encrypted_text)
    
    # Расшифрование для проверки
    decrypted_text = cipher.decrypt(encrypted_text)
    print(f"\n3. РАСШИФРОВАННЫЙ ТЕКСТ (для проверки):")
    print("-"*70)
    print(decrypted_text)
    
    # Проверка корректности
    if original_text.lower() == decrypted_text.lower():
        print("\n✓ ПРОВЕРКА: Расшифрованный текст совпадает с исходным!")
    else:
        print("\n✗ ПРОВЕРКА: Ошибка расшифрования!")
    
    # Частотный анализ
    print("\n4. ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА:")
    freq = analyzer.analyze(encrypted_text)
    analyzer.print_frequency_table(freq)
    
    # Сохранение результатов
    with open(f'{RESULTS_DIR}/task1_original.txt', 'w', encoding='utf-8') as f:
        f.write(original_text)
    
    with open(f'{RESULTS_DIR}/task1_encrypted.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_text)
    
    with open(f'{RESULTS_DIR}/task1_key.txt', 'w', encoding='utf-8') as f:
        f.write(f"Ключ шифрования (сдвиг): {cipher.get_shift()}\n")
    
    analyzer.save_frequency_table(freq, f'{RESULTS_DIR}/task1_frequency.txt')
    
    print(f"\n✓ Результаты задания 1 сохранены в папку '{RESULTS_DIR}/'")
    print("\nФайлы:")
    print("  - task1_original.txt")
    print("  - task1_encrypted.txt")
    print("  - task1_key.txt")
    print("  - task1_frequency.txt")
    
    return cipher, analyzer


if __name__ == "__main__":
    run_task1()