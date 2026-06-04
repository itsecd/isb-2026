<<<<<<< HEAD
﻿import path_file as pf

def caesar_cipher(text, shift):
=======
﻿def caesar_cipher(text, shift):
>>>>>>> 2ab1c3a8a7fc68eb2b4b8e12e4181499f6e590f9
    """Шифрует или дешифрует текст алгоритмом Цезаря"""
    result = []
    for char in text:
        code = ord(char)
        
        if 0x0410 <= code <= 0x042F:
            new_code = ((code - 0x0410 + shift) % 32) + 0x0410
            result.append(chr(new_code))
        elif 0x0430 <= code <= 0x044F:
            new_code = ((code - 0x0430 + shift) % 32) + 0x0430
            result.append(chr(new_code))
        elif 0x0041 <= code <= 0x005A:
            new_code = ((code - 0x0041 + shift) % 26) + 0x0041
            result.append(chr(new_code))
        elif 0x0061 <= code <= 0x007A:
            new_code = ((code - 0x0061 + shift) % 26) + 0x0061
            result.append(chr(new_code))
        elif 0x0030 <= code <= 0x0039:
            new_code = ((code - 0x0030 + shift) % 10) + 0x0030
            result.append(chr(new_code))
        else:
            result.append(char)
    
    return "".join(result)

def generate_substitution_key(shift):
    """Генерирует полный ключ подстановки"""
    key = {}
    
    for i in range(32):
        original = chr(0x0410 + i)
        shifted = chr(((i + shift) % 32) + 0x0410)
        key[original] = shifted
    
    for i in range(32):
        original = chr(0x0430 + i)
        shifted = chr(((i + shift) % 32) + 0x0430)
        key[original] = shifted
    
    for i in range(26):
        original = chr(0x0041 + i)
        shifted = chr(((i + shift) % 26) + 0x0041)
        key[original] = shifted
    
    for i in range(26):
        original = chr(0x0061 + i)
        shifted = chr(((i + shift) % 26) + 0x0061)
        key[original] = shifted
    
    for i in range(10):
        original = chr(0x0030 + i)
        shifted = chr(((i + shift) % 10) + 0x0030)
        key[original] = shifted
    
    return key

def read_file(filename):
    """Читает текст из файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, text):
    """Записывает текст в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def write_key(filename, key, shift):
    """Записывает ключ шифрования в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Сдвиг: {shift}\n\n")
        
        for original, shifted in sorted(key.items()):
            f.write(f"{original}={shifted}\n")

def main():
    """Главная функция для задания 1"""
    print("ЗАДАНИЕ 1: ШИФРОВКА И ДЕШИФРОВКА ТЕКСТА АЛГОРИТМОМ ЦЕЗАРЯ")
    
<<<<<<< HEAD
=======
    input_file = 'input_text.txt'
    output_encrypted = 'encrypted_task1.txt'
    output_key = 'key_task1.txt'
    
>>>>>>> 2ab1c3a8a7fc68eb2b4b8e12e4181499f6e590f9
    try:
        KEY = int(input("Введите ключ шифрования (сдвиг): "))
    except ValueError:
        print("Ошибка: ключ должен быть числом!")
        return
    
    try:
<<<<<<< HEAD
        original_text = read_file(pf.INPUT_FILE)
    except FileNotFoundError:
        print(f"Файл '{pf.INPUT_FILE}' не найден!")
=======
        original_text = read_file(input_file)
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден!")
>>>>>>> 2ab1c3a8a7fc68eb2b4b8e12e4181499f6e590f9
        return
    
    substitution_key = generate_substitution_key(KEY)
    
    encrypted_text = caesar_cipher(original_text, KEY)
    print(f"Текст зашифрован (ключ: {KEY})")
    
<<<<<<< HEAD
    write_file(pf.OUTPUT_ENCRYPTED, encrypted_text)
    write_key(pf.OUTPUT_KEY, substitution_key, KEY)
    print(f"  - {pf.OUTPUT_ENCRYPTED} (зашифрованный текст)")
    print(f"  - {pf.OUTPUT_KEY} (ключ шифрования с таблицей подстановки)")
=======
    write_file(output_encrypted, encrypted_text)
    write_key(output_key, substitution_key, KEY)
    print(f"  - {output_encrypted} (зашифрованный текст)")
    print(f"  - {output_key} (ключ шифрования с таблицей подстановки)")
>>>>>>> 2ab1c3a8a7fc68eb2b4b8e12e4181499f6e590f9
    
    decrypted_text = caesar_cipher(encrypted_text, -KEY)
    print(f"Текст дешифрован (ключ: {-KEY})")
    
    if decrypted_text == original_text:
        print("Расшифрованный текст совпадает с исходным!")
    else:
        print("Расшифрованный текст не совпадает с исходным!")

if __name__ == "__main__":
    main()