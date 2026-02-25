def load_key_from_table(filename: str) -> dict[str, str]:
    """Читает таблицу Полибия из файла и возвращает словарь буква → код."""
    key = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) < 7:
                continue
            row = parts[0]
            letters = parts[1:7]
            for col, letter in enumerate(letters, start=1):
                if letter == 'пробел':
                    letter = ' '
                if letter != '-':
                    code = row + str(col)
                    key[letter] = code
        return key

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с ключом '{filename}' не найден.")
    except Exception:
        raise ValueError("Ошибка при чтении файла ключа.")


def encrypt_text(text: str, key: dict[str, str]) -> str:
    """Шифрует текст с использованием переданного ключа."""
    encrypted_parts = []
    for ch in text:
        if ch in key:
            encrypted_parts.append(key[ch])
        else:
            raise ValueError(f"Символ '{ch}' отсутствует в ключе шифрования.")
    return ' '.join(encrypted_parts)


def decrypt_text(encrypted_text: str, key: dict[str, str]) -> str:
    """Дешифрует текст с использованием переданного ключа."""
    reverse_key = {v: k for k, v in key.items()}
    decrypted_parts = []
    for code in encrypted_text.split():
        if code in reverse_key:
            decrypted_parts.append(reverse_key[code])
        else:
            raise ValueError(f"Код '{code}' отсутствует в ключе дешифрования.")
    return ''.join(decrypted_parts)


def save_to_file(filename: str, content: str) -> None:
    """Сохраняет содержимое в файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def main() -> None:
    """Основная функция: шифрование, проверка и сохранение результатов."""
    try:
        key_file = 'key.txt'
        print(f"Загрузка ключа из '{key_file}'...")
        key = load_key_from_table(key_file)

        input_file = 'input_text.txt'
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{input_file}' не найден.")

        encrypted = encrypt_text(text, key)

        encrypted_file = 'encrypted.txt'
        save_to_file(encrypted_file, encrypted)
        print(f"Зашифрованный текст сохранён в '{encrypted_file}'.")

        decrypted = decrypt_text(encrypted, key)

        decrypted_file = 'decrypted_check.txt'
        save_to_file(decrypted_file, decrypted)
        print(f"Расшифрованный текст сохранён в '{decrypted_file}'.")

        if decrypted == text:
            print("Расшифрованный текст совпадает с исходным.")
        else:
            print("Расшифрованный текст отличается от исходного!")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except ValueError as e:
        print(f"Ошибка в данных: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()