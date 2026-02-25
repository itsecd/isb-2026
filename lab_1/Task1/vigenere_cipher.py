# -*- coding: utf-8 -*-
def main():
    """Основная функция для шифрования и расшифровки текста методом Виженера"""
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
    key = 'КРИПТОГРАФИЯ'
    
    try:
        with open('original.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("Ошибка: файл original.txt не найден")
        print("Создайте файл original.txt с текстом для шифрования")
        return
    except IOError as e:
        print(f"Ошибка при чтении файла original.txt: {e}")
        return
    
    if not text:
        print("Ошибка: файл original.txt пуст")
        return
    
    try:
        text = text.upper()
        key_indices = [alphabet.index(k) for k in key]
    except ValueError as e:
        print(f"Ошибка: символ не найден в алфавите - {e}")
        return
    
    result = []
    for i, char in enumerate(text):
        if char in alphabet:
            char_index = alphabet.index(char)
            key_index = key_indices[i % len(key)]
            result.append(alphabet[(char_index + key_index) % len(alphabet)])
        else:
            result.append(char)
    
    encrypted_text = ''.join(result)
    
    try:
        with open('encrypted.txt', 'w', encoding='utf-8') as f:
            f.write(encrypted_text)
        with open('key.txt', 'w', encoding='utf-8') as f:
            f.write(key)
    except IOError as e:
        print(f"Ошибка при записи файлов: {e}")
        return
    
    decrypted = []
    for i, char in enumerate(encrypted_text):
        if char in alphabet:
            char_index = alphabet.index(char)
            key_index = key_indices[i % len(key)]
            decrypted.append(alphabet[(char_index - key_index) % len(alphabet)])
        else:
            decrypted.append(char)
    
    try:
        with open('check.txt', 'w', encoding='utf-8') as f:
            f.write(''.join(decrypted))
    except IOError as e:
        print(f"Ошибка при записи файла check.txt: {e}")
        return
    
    print("Созданы файлы: encrypted.txt, key.txt, check.txt")
    print("Исходный текст прочитан из файла: original.txt")

if __name__ == '__main__':
    main()
