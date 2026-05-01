from pathlib import Path
from vigenere import vigenere_encrypt, vigenere_decrypt, read_key_from_file

BASE_DIR = Path(__file__).resolve().parent


def main():
    """Запускает процесс шифрования и проверки расшифровки."""
    try:
        key_path = BASE_DIR / "key.txt"
        input_path = BASE_DIR / "input.txt"
        encrypted_path = BASE_DIR / "encrypted.txt"

        key = read_key_from_file(key_path)
        print(f"Ключ прочитан из файла: {key}")

        if not input_path.exists():
            print(f"Ошибка: файл '{input_path.name}' не найден!")
            return

        original_text = input_path.read_text(encoding="utf-8")
        print("Исходный текст прочитан из файла input.txt")

        encrypted = vigenere_encrypt(original_text, key)

        encrypted_path.write_text(encrypted, encoding="utf-8")
        print("Зашифрованный текст сохранен в файл 'encrypted.txt'")

        print("\n" + "=" * 50)
        print("ЗАШИФРОВАННЫЙ ТЕКСТ:")
        print("=" * 50)
        print(encrypted)
        print("=" * 50)

        decrypted = vigenere_decrypt(encrypted, key)

        print("\nРАСШИФРОВАННЫЙ ТЕКСТ (для проверки):")
        print("=" * 50)
        print(decrypted)
        print("=" * 50)

        if decrypted == original_text:
            print("\n✓ Проверка пройдена: расшифрованный текст совпадает с исходным")
        else:
            print("\n✗ Внимание: расшифрованный текст НЕ совпадает с исходным!")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()