ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '


def encode_text(text, shift):
    """
    Шифрует текст методом Цезаря
    Args:
        text (str): исходный текст
        shift (int): величина сдвига
    Returns:
        str: зашифрованный текст
    """
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
    """
    Дешифрует текст методом Цезаря
    Args:
        cipher_text (str): зашифрованный текст
        shift (int): величина сдвига
    Returns:
        str: исходный текст
    """
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


def load_file(filename):
    """
    Загружает текст из файла
    Args:
        filename (str): имя файла
    Returns:
        str: содержимое файла
    Raises:
        FileNotFoundError: если файл не найден
        IOError: если ошибка чтения
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        raise
    except IOError as e:
        print(f"Ошибка чтения файла: {e}")
        raise


def save_file(filename, content):
    """
    Сохраняет текст в файл
    Args:
        filename (str): имя файла
        content (str): данные для записи
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        print(f"Ошибка записи в {filename}: {e}")


def check_result(original_text, decrypted_text):
    """
    Проверяет корректность шифрования и дешифрования
    Args:
        original_text (str): исходный текст
        decrypted_text (str): результат расшифровки
    Returns:
        bool: True если совпадает
    """
    return original_text.upper() == decrypted_text.upper()


def main():
    try:
        shift = int(input("Введите сдвиг (ключ Цезаря): "))
    except ValueError:
        print("Ошибка: нужно ввести целое число")
        return

    try:
        text = load_file("original_task1.txt")
    except Exception:
        return

    encrypted = encode_text(text, shift)
    decrypted = decode_text(encrypted, shift)

    save_file("encrypted_task1.txt", encrypted)
    save_file("decrypted_task1.txt", decrypted)

    key_info = (
        f"ШИФР Цезаря\n"
        f"АЛФАВИТ: {ALPHABET}\n"
        f"СДВИГ: {shift}\n"
        f"ПРОВЕРКА: {check_result(text, decrypted)}"
    )

    save_file("key_task1.txt", key_info)

    print("\nПРОВЕРКА:")
    print("Совпадение:", check_result(text, decrypted))

    print("\nПервые 100 символов:")
    print(decrypted[:100])


if __name__ == "__main__":
    main()
