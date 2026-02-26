"""
Модуль для расшифровки текста, анализа частоты символов и работы с файлами.

Скрипт предназначен для обработки зашифрованных файлов с использованием
ключа подстановки, сохраненного в формате словаря Python.
"""

import ast
from collections import Counter


def decrypt_text(key: str, text: str) -> str:
    """
    Расшифровывает текст, используя ключ подстановки.

    Ключ должен быть строковым представлением словаря Python (например, "{'a': 'b'}"),
    который безопасно вычисляется с помощью ast.literal_eval.

    Args:
        key (str): Строковое представление словаря маппинга символов.
        text (str): Зашифрованный текст.

    Returns:
        str: Расшифрованный plaintext.
    """
    crypto_key = ast.literal_eval(key)
    plaintext = "".join(crypto_key.get(char, char) for char in text)
    return plaintext


def get_freq(text: str) -> str:
    """
    Вычисляет частоту встречаемости каждого символа в тексте.

    Символы сортируются по убыванию частоты. Результат возвращается
    в виде строкового представления словаря.

    Args:
        text (str): Исходный текст для анализа.

    Returns:
        str: Строковое представление словаря {символ: частота}.
    """
    if not text:
        return "{}"

    len_t = len(text)
    # Используем Counter для оптимизации (O(N) вместо O(N^2))
    char_counts = Counter(text)

    # Вычисляем относительную частоту и сортируем
    char_freq = {char: count / len_t for char, count in char_counts.items()}
    freq_char = dict(
        sorted(char_freq.items(), key=lambda item: item[1], reverse=True)
    )

    return str(freq_char)


def write_file(path: str, text: str) -> None:
    """
    Записывает текст в указанный файл.

    Файл создается или перезаписывается. Кодировка: UTF-8.

    Args:
        path (str): Путь к файлу для записи.
        text (str): Текст, который необходимо записать.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def open_file(path: str) -> str:
    """
    Считывает содержимое файла.

    Args:
        path (str): Путь к файлу для чтения.

    Returns:
        str: Содержимое файла.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    """
    Основная функция выполнения скрипта.

    Считывает зашифрованный текст и ключ, расшифровывает сообщение,
    выводит результат в консоль, а также сохраняет частотный анализ
    и расшифрованный текст в отдельные файлы.
    """
    encrypted_text = open_file("cod13.txt")
    key = open_file("key1.txt")

    print(f"Зашифрованный текст:\n{encrypted_text}\n")

    decrypted = decrypt_text(key, encrypted_text)
    print(f"Расшифрованный текст:\n{decrypted}")

    write_file("frequency.txt", get_freq(encrypted_text))
    write_file("decrypted_2.txt", decrypted)


if __name__ == "__main__":
    main()