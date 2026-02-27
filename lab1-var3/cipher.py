ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

def caesar_encrypt(text, shift):
    # Шифрование текста шифром Цезаря
    result = []
    for char in text:
        upper_char = char.upper()
        if upper_char in ALPHABET:
            idx = ALPHABET.index(upper_char)
            new_idx = (idx + shift) % len(ALPHABET)
            result.append(ALPHABET[new_idx])
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(encrypted_text, shift):
    # Дешифрование текста, зашифрованного шифром Цезаря
    result = []
    for char in encrypted_text:
        upper_char = char.upper()
        if upper_char in ALPHABET:
            idx = ALPHABET.index(upper_char)
            new_idx = (idx - shift) % len(ALPHABET)
            result.append(ALPHABET[new_idx])
        else:
            result.append(char)
    return ''.join(result)

def verify_encryption(original_text, shift):
    # Проверка корректности шифрования путем дешифрования
    encrypted = caesar_encrypt(original_text, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    
    if original_text == decrypted:
        print("Проверка пройдена: расшифрованный текст совпадает с исходным")
        return True, decrypted
    else:
        print("Ошибка: расшифрованный текст не совпадает с исходным!")
        print(f"Исходный текст (первые 50 символов): {original_text[:50]}")
        print(f"Расшифрованный (первые 50 символов): {decrypted[:50]}")
        return False, decrypted

def main():
    # Основная функция программы
    try:
        # Ввод сдвига
        try:
            SHIFT = int(input("Введите сдвиг для шифра Цезаря: "))
        except ValueError:
            print("Ошибка: сдвиг должен быть числом!")
            return

        # Чтение файла
        try:
            with open('input_text.txt', 'r', encoding='utf-8') as f:
                original_text = f.read()
        except FileNotFoundError:
            print('=' * len('Ошибка: файл input_text.txt не найден!'))
            print("\nОшибка: файл input_text.txt не найден!")
            print("Создайте файл input_text.txt с исходным текстом\n")
            return
        except IOError as e:
            print(f"Ошибка при чтении файла: {e}")
            return

        # Информация о тексте
        text_length = len(original_text)
        print('=' * len('Текст загружен, длина:        символов'))
        print(f"Текст загружен, длина: {text_length} символов")
        print('=' * len('Текст загружен, длина:        символов'))

        # Шифрование
        encrypted_text = caesar_encrypt(original_text, SHIFT)
        
        # Проверка дешифрованием
        print("\n--- Проверка корректности алгоритма ---")
        verification_passed, decrypted_text = verify_encryption(original_text, SHIFT)
        print("----------------------------------------\n")

        # Сохранение результатов
        try:
            # Сохраняем зашифрованный текст
            with open('encrypted.txt', 'w', encoding='utf-8') as f:
                f.write(encrypted_text)
            print("Зашифрованный текст сохранен в файл encrypted.txt")
            
            # Сохраняем расшифрованный текст (для проверки)
            with open('decrypted.txt', 'w', encoding='utf-8') as f:
                f.write(decrypted_text)
            print("Расшифрованный текст сохранен в файл decrypted.txt")

            # Сохраняем ключ и информацию
            with open('key.txt', 'w', encoding='utf-8') as f:
                f.write(f'Шифр: Цезарь\n')
                f.write(f'Алфавит: {ALPHABET}\n')
                f.write(f'Сдвиг: {SHIFT}\n')
                f.write(f'Проверка дешифрованием: {"успешна" if verification_passed else "провалена"}\n')
                f.write('Таблица замены (исходный символ -> зашифрованный):\n')
                f.write('=' * 50 + '\n')
                for i, char in enumerate(ALPHABET):
                    new_char = ALPHABET[(i + SHIFT) % len(ALPHABET)]
                    if char == ' ':
                        f.write(f'ПРОБЕЛ -> {new_char}\n')
                    else:
                        f.write(f'{char} -> {new_char}\n')
            print("Ключевая информация сохранена в файл key.txt")
            
        except IOError as e:
            print(f"Ошибка при сохранении файлов: {e}")
            return

        # Вывод результата
        print(f"\nЗашифрованный текст (первые 100 символов):\n")
        print(f"{encrypted_text[:100]}...")
        print(f"\nРасшифрованный текст (первые 100 символов):\n")
        print(f"{decrypted_text[:100]}...")
        
        if verification_passed:
            print("\nАлгоритм работает корректно! Расшифрованный текст совпадает с исходным.")
        else:
            print("\nОбнаружена проблема с алгоритмом!")
        print("\n")
        print('=' * len('Готово!'))
        print(f"Готово! Все файлы сохранены.")
        print('=' * len('Готово!'))

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()