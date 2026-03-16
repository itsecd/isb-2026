def caesar_cipher_russian(text, shift):
    """
    Функция для шифрования текста с помощью шифра Цезаря (русский алфавит, верхний регистр)
    
    Аргументы:
    text (str): Текст для шифрования
    shift (int): Количество позиций для сдвига букв
    
    Возвращает:
    tuple: (зашифрованный_текст, ключ_шифрования)
    """
    # Русский алфавит (включая Ё)
    russian_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    alphabet_size = len(russian_alphabet)
    
    # Создаем ключ шифрования
    key_map = {}
    for i, letter in enumerate(russian_alphabet):
        shifted_index = (i + shift) % alphabet_size
        key_map[letter] = russian_alphabet[shifted_index]
        # Также добавляем строчную букву в ключ
        key_map[letter.lower()] = russian_alphabet[shifted_index]
    
    # Преобразуем входной текст в верхний регистр
    text = text.upper()
    
    # Шифруем текст
    encrypted_text = ""
    for char in text:
        if char in key_map:
            # Если это буква русского алфавита - применяем шифр
            encrypted_text += key_map[char]
        else:
            # Если это не буква (пробел, знак препинания и т.д.) - оставляем без изменений
            encrypted_text += char
    
    return encrypted_text, key_map


def display_key(key_map):
    """
    Функция для отображения ключа шифрования
    """
    print("Ключ шифрования (оригинал -> зашифрованная буква):")
    print("-" * 50)
    
    # Отображаем только заглавные буквы
    russian_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    for letter in russian_alphabet:
        print(f"{letter}->{key_map[letter]}", end="  ")
        # Делаем перенос строки каждые 7 пар для лучшей читаемости
        if (russian_alphabet.index(letter) + 1) % 7 == 0:
            print()
    
    print("\n" + "-" * 50)


# Пример использования:
if __name__ == "__main__":
    # Текст для шифрования
    original_text = input("Введите текст для шифрования: ")
    shift_value = int(input("Введите сдвиг (целое число): "))
    
    # Шифрование
    encrypted_result, encryption_key = caesar_cipher_russian(original_text, shift_value)
    
    # Вывод результата
    print(f"\nИсходный текст: {original_text.upper()}")
    print(f"Зашифрованный текст: {encrypted_result}")
    print(f"\nСдвиг: {shift_value}")
    
    # Отображение ключа
    display_key(encryption_key)x`x
