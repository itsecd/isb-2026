"""Модуль: шифр Цезаря для русского алфавита."""

ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

def encode_text(text, shift):
    """Зашифровать текст сдвигом Цезаря."""
    result = []
    for symbol in text:
        upper_symbol = symbol.upper()
        if upper_symbol in ALPHABET:
            pos = ALPHABET.index(upper_symbol)
            new_pos = (pos + shift) % len(ALPHABET)
            result.append(ALPHABET[new_pos])
        else:
            result.append(symbol)
    return ''.join(result)

def decode_text(cipher_text, shift):
    """Дешифровать текст сдвигом Цезаря."""
    result = []
    for symbol in cipher_text:
        upper_symbol = symbol.upper()
        if upper_symbol in ALPHABET:
            pos = ALPHABET.index(upper_symbol)
            new_pos = (pos - shift) % len(ALPHABET)
            result.append(ALPHABET[new_pos])
        else:
            result.append(symbol)
    return ''.join(result)

def check_result(source_text, shift):
    """Проверить, что дешифровка возвращает исходный текст."""
    encrypted = encode_text(source_text, shift)
    decrypted = decode_text(encrypted, shift)

    if source_text.upper() == decrypted:
        print("Проверка выполнена успешно: тексты совпадают")
        return True, decrypted
    else:
        print("Проверка не пройдена: обнаружены различия")
        print(f"Оригинал (первые 50 символов): {source_text[:50]}")
        print(f"Результат (первые 50 символов): {decrypted[:50]}")
        return False, decrypted

def run_program():
    """CLI: выполнить шифрование файла `input_text.txt` и сохранить результаты."""
    try:
        try:
            shift_value = int(input("Введите величину сдвига: "))
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")
            return

        try:
            with open('input_text.txt', 'r', encoding='utf-8') as file:
                source_text = file.read()
        except FileNotFoundError:
            print("\nФайл input_text.txt отсутствует.")
            print("Создайте его и поместите туда исходный текст.\n")
            return
        except IOError as error:
            print(f"Ошибка чтения файла: {error}")
            return

        text_size = len(source_text)

        print('=' * 40)
        print(f"Файл успешно загружен. Размер текста: {text_size} символов")
        print('=' * 40)

        cipher_text = encode_text(source_text, shift_value)

        print("\nПроверка алгоритма")
        print('-' * 40)

        success, restored_text = check_result(source_text, shift_value)

        print('-' * 40)

        try:
            with open('encrypted.txt', 'w', encoding='utf-8') as file:
                file.write(cipher_text)
            print("Файл encrypted.txt сохранён")

            with open('decrypted.txt', 'w', encoding='utf-8') as file:
                file.write(restored_text)
            print("Файл decrypted.txt сохранён")

            with open('key.txt', 'w', encoding='utf-8') as file:
                file.write('Шифр: Цезаря\n')
                file.write(f'Алфавит: {ALPHABET}\n')
                file.write(f'Ключ (сдвиг): {shift_value}\n')
                file.write(f'Результат проверки: {"успешно" if success else "ошибка"}\n')
                file.write('Таблица преобразования символов:\n')
                file.write('=' * 50 + '\n')

                for i, symbol in enumerate(ALPHABET):
                    encoded_symbol = ALPHABET[(i + shift_value) % len(ALPHABET)]

                    if symbol == ' ':
                        file.write(f'ПРОБЕЛ -> {encoded_symbol}\n')
                    else:
                        file.write(f'{symbol} -> {encoded_symbol}\n')

            print("Информация о ключе записана в key.txt")

        except IOError as error:
            print(f"Ошибка записи файлов: {error}")
            return

        print("\nПервые 100 символов шифротекста:\n")
        print(f"{cipher_text[:100]}...")

        print("\nПервые 100 символов восстановленного текста:\n")
        print(f"{restored_text[:100]}...")

        if success:
            print("\nРабота программы подтверждена.")
        else:
            print("\nПри проверке были обнаружены ошибки.")

        print("\n" + '=' * 30)
        print("Обработка завершена.")
        print('=' * 30)

    except Exception as error:
        print(f"Непредвиденная ошибка: {error}")

if __name__ == "__main__":
    run_program()