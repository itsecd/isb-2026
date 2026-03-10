# task1_encrypt.py
"""
Задание 1: Шифрование текста шифром простой подстановки
"""

import random
from utils import RUS_ALPHABET, ALPHABET_LEN, clean_text, write_file, read_file

def generate_random_key():
    shuffled = list(RUS_ALPHABET)
    random.shuffle(shuffled)
    
    key = {}
    for i, char in enumerate(RUS_ALPHABET):
        key[char] = shuffled[i]
    
    return key

def save_key(key, filename):
    lines = ["КЛЮЧ ШИФРОВАНИЯ (моноалфавитная замена):",
             "Исходная буква -> Зашифрованная буква",
             "-" * 40]
    
    for original, encrypted in sorted(key.items()):
        orig_display = 'ПРОБЕЛ' if original == ' ' else original
        enc_display = 'ПРОБЕЛ' if encrypted == ' ' else encrypted
        lines.append(f"{orig_display:6} -> {enc_display}")
    
    write_file(filename, '\n'.join(lines))

def encrypt(text, key):
    encrypted = []
    for char in text:
        if char in key:
            encrypted.append(key[char])
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def main():
    print("=" * 50)
    print("ЗАДАНИЕ 1: ШИФРОВАНИЕ ТЕКСТА")
    print("=" * 50)
    
    original_text = read_file("data/task1/original.txt")
    if original_text is None:
        print("\nСоздайте файл data/task1/original.txt с текстом (не менее 500 символов)")
        sample_text = """Криптография - это наука о методах обеспечения конфиденциальности, 
целостности данных, аутентификации, а также невозможности отказа от авторства. 
Изначально криптография изучала методы шифрования информации - обратимого 
преобразования открытого текста в шифрованный на основе секретного ключа. 
Традиционно криптография делится на симметричную и асимметричную. 
В симметричной криптографии один и тот же ключ используется как для шифрования, 
так и для расшифрования данных. В асимметричной криптографии используются два 
ключа: открытый и закрытый. Открытый ключ может публиковаться и используется 
для шифрования данных, а закрытый ключ держится в секрете и используется для 
расшифрования. Шифр простой замены - один из самых древних методов шифрования, 
где каждая буква исходного текста заменяется на другую букву того же алфавита 
по определенному правилу. Этот шифр легко взламывается с помощью частотного 
анализа, так как частоты появления букв в языке хорошо известны. Например, 
в русском языке самая частая буква - О, затем И, Е, А и так далее. Пробел 
вообще самый частый символ в любом тексте."""
        print(sample_text)
        write_file("data/task1/original.txt", sample_text)
        original_text = sample_text
    
    cleaned_text = clean_text(original_text)
    print(f"\nИсходный текст (очищенный):")
    print(f"Длина: {len(cleaned_text)} символов")
    print(f"Первые 200 символов: {cleaned_text[:200]}...")
    
    if len(cleaned_text) < 500:
        print(f"\nВНИМАНИЕ: Длина текста {len(cleaned_text)} < 500 символов!")
        print("Добавьте текст в файл data/task1/original.txt")
        return
    
    key = generate_random_key()
    
    encrypted_text = encrypt(cleaned_text, key)
    
    write_file("data/task1/encrypted.txt", encrypted_text)
    save_key(key, "data/task1/key.txt")
    
    print(f"\nРезультаты сохранены:")
    print(f"  - Зашифрованный текст: data/task1/encrypted.txt")
    print(f"  - Ключ шифрования: data/task1/key.txt")
    
    print(f"\nДемонстрация (первые 100 символов):")
    print(f"Оригинал:  {cleaned_text[:100]}")
    print(f"Шифр:      {encrypted_text[:100]}")
    
    reverse_key = {v: k for k, v in key.items()}
    decrypted_check = encrypt(encrypted_text, reverse_key)
    if decrypted_check == cleaned_text:
        print(f"\n✓ Проверка пройдена: текст успешно расшифровывается обратно")
    else:
        print(f"\n✗ Ошибка: текст не совпадает при расшифровке")

if __name__ == "__main__":
    main()