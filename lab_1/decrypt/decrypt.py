import collections
import sys
import constants


def analyze_and_create_key(cipher_text: str, freq_file: str, key_file: str) -> dict:
    """
    Вычисляет частоты символов в шифротексте, сохраняет их и генерирует первичный ключ.

    Очищает текст от символов переноса строк, подсчитывает частоту каждого оставшегося
    символа и сопоставляет самые частые символы шифра с эталонными частотами языка.

    Args:
        cipher_text (str): Исходный зашифрованный текст.
        freq_file (str): Путь к файлу для сохранения статистики частот.
        key_file (str): Путь к файлу для сохранения сгенерированного ключа.

    Returns:
        dict: Базовый словарь подстановок (символ_шифра -> буква_языка).

    Raises:
        ValueError: Если после очистки текста от переносов он оказался пустым.
        IOError: При ошибке записи в файлы статистики или ключа.
    """
    clean_text = cipher_text.replace('\n', '').replace('\r', '')
    if not clean_text:
        raise ValueError("Ошибка: Текст не содержит валидных символов для анализа.")

    counter = collections.Counter(clean_text)
    total_chars = sum(counter.values())

    sorted_cipher_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    try:
        with open(freq_file, "w", encoding="utf-8") as f:
            f.write("Символ -> Частота -> Количество\n")
            f.write("-" * 35 + "\n")
            for char, count in sorted_cipher_freqs:
                freq = count / total_chars
                display_char = repr(char) if char.isspace() else char
                f.write(f"{display_char:<8} -> {freq:.6f} -> {count}\n")
    except IOError as e:
        raise IOError(f"Не удалось сохранить статистику частот в файл '{freq_file}': {e}")

    key = {}
    try:
        with open(key_file, "w", encoding="utf-8") as f:
            for i, (cipher_char, _) in enumerate(sorted_cipher_freqs):
                if i < len(constants.REFERENCE_FREQS):
                    plain_char = constants.REFERENCE_FREQS[i]
                    key[cipher_char] = plain_char
                    f.write(f"{cipher_char} -> {plain_char}\n")
    except IOError as e:
        raise IOError(f"Не удалось сохранить первичный ключ в файл '{key_file}': {e}")

    return key


def decrypt(text: str, key: dict) -> str:
    """
    Расшифровывает текст с использованием переданного словаря подстановок.

    Args:
        text (str): Зашифрованный текст.
        key (dict): Словарь, где ключ - символ шифра, значение - буква открытого текста.

    Returns:
        str: Расшифрованный текст. Если символ отсутствует в ключе, он остается без изменений.
    """
    return "".join(key.get(c, c) for c in text)


def load_key(filepath: str) -> dict:
    """
    Загружает словарь подстановок (ключ) из текстового файла.

    Ожидается формат строк: 'символ_шифра -> символ_языка'.

    Args:
        filepath (str): Путь к файлу ключа.

    Returns:
        dict: Загруженный словарь подстановок.

    Raises:
        FileNotFoundError: Если указанный файл ключа не существует.
        IOError: При ошибке чтения файла.
    """
    key = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if " -> " in line:
                    parts = line.split(" -> ")
                    if len(parts) == 2:
                        cipher_char = parts[0]
                        plain_char = parts[1].strip('\n\r')
                        if not plain_char:
                            plain_char = " "
                        key[cipher_char] = plain_char
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл ключа '{filepath}' не найден.")
    except IOError as e:
        raise IOError(f"Ошибка чтения файла ключа '{filepath}': {e}")

    return key


def main():
    """
    Точка входа в программу. Оркестрирует процессы чтения файлов,
    анализа частот, генерации ключа и расшифровки.
    """
    try:
        with open(constants.INPUT_FILE, "r", encoding="utf-8") as f:
            cipher_text = f.read()
    except FileNotFoundError:
        print(f"Критическая ошибка: Входной файл '{constants.INPUT_FILE}' не найден.")
        sys.exit(1)
    except IOError as e:
        print(f"Критическая ошибка: Не удалось прочитать '{constants.INPUT_FILE}': {e}")
        sys.exit(1)

    try:
        key = analyze_and_create_key(cipher_text, constants.FREQ_FILE, constants.KEY_FILE)

        result = decrypt(cipher_text, key)

        with open(constants.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(result)

    except (ValueError, IOError, FileNotFoundError) as e:
        print(f"\nОшибка выполнения: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()