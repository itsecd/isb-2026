import os
import sys

INPUT_FILE = "encrypted.txt"
OUTPUT_FILE = "decrypted.txt"
KEY_FILE = "cipher_key.txt"
RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def load_key(key_file_path: str) -> dict:
    """
    Читает ключ шифрования из файла и возвращает таблицу трансляции (maketrans).

    Args:
        key_file_path: путь к файлу с ключом шифрования

    Returns:
        словарь-перевод (результат str.maketrans) для метода .translate()

    Raises:
        SystemExit: если файл не найден, формат неверный или длины алфавитов различаются
    """
    if not os.path.exists(key_file_path):
        print(f"Ошибка: файл с ключом '{key_file_path}' не найден")
        sys.exit(1)

    with open(key_file_path, encoding="utf-8") as f:
        line = f.read().strip()

    if " → " not in line:
        print("Ошибка формата ключа")
        sys.exit(1)

    original, _, encrypted = line.partition(" → ")
    original = original.strip()
    encrypted = encrypted.strip()

    if len(original) != len(encrypted):
        print("Ошибка в ключе: разная длина алфавитов")
        sys.exit(1)

    if original != RUSSIAN_ALPHABET:
        print("Внимание: исходный алфавит в ключе не совпадает с ожидаемым")

    return str.maketrans(encrypted, original)


def decrypt_file(input_path: str, output_path: str, trans_table: dict) -> None:
    '''Выполняет расшифровку файла с зашифрованным текстом и сохраняет результат.

    Args:
        input_path: путь к файлу с зашифрованным текстом
        output_path: путь, куда будет сохранён расшифрованный текст
        trans_table: таблица трансляции (dict), полученная из str.maketrans

    Raises:
        SystemExit: если входной файл не найден
    '''
    if not os.path.exists(input_path):
        print(f"Ошибка: файл '{input_path}' не найден")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        encrypted_text = f.read()

    decrypted_text = encrypted_text.translate(trans_table)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decrypted_text)

    print(f"Расшифрованный текст сохранён в: {output_path}")


def main() -> None:
    '''
    Загружает ключ шифрования
    Расшифровывает входной файл
    Сохраняет результат в выходной файл
    '''
    print("Программа расшифровки текста (моноалфавитная замена)")
    print(f"Используется ключ из файла: {KEY_FILE}\n")

    try:
        trans_table = load_key(KEY_FILE)
        decrypt_file(INPUT_FILE, OUTPUT_FILE, trans_table)
        print("Расшифровка завершена успешно.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()