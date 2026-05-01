"""Модуль шифрования и дешифрования Виженера."""

from constants import RUS_ALPHABET, RUS_ALPHABET_UPPER, ALPHABET_LENGTH
from pathlib import Path


def _clean_key(key: str) -> str:
    """Удаляет из ключа все символы кроме русских букв."""
    return "".join(c for c in key.lower() if c in RUS_ALPHABET)


def _find_pos(alphabet: str, char: str) -> int:
    """Возвращает индекс символа в алфавите."""
    pos = 0
    while pos < len(alphabet) and alphabet[pos] != char:
        pos += 1
    return pos


def vigenere_encrypt(text: str, key: str) -> str:
    """Шифрует текст шифром Виженера."""
    clean_key = _clean_key(key)
    if not clean_key:
        return "Ошибка: ключ должен содержать буквы русского алфавита"

    result = ""
    key_index = 0

    for char in text:

        if char in RUS_ALPHABET:
            pos = _find_pos(RUS_ALPHABET, char)
            key_pos = _find_pos(RUS_ALPHABET, clean_key[key_index])

            result += RUS_ALPHABET[(pos + key_pos) % ALPHABET_LENGTH]
            key_index = (key_index + 1) % len(clean_key)

        elif char in RUS_ALPHABET_UPPER:
            pos = _find_pos(RUS_ALPHABET_UPPER, char)
            key_pos = _find_pos(RUS_ALPHABET, clean_key[key_index])

            result += RUS_ALPHABET_UPPER[(pos + key_pos) % ALPHABET_LENGTH]
            key_index = (key_index + 1) % len(clean_key)

        else:
            result += char

    return result


def vigenere_decrypt(text: str, key: str) -> str:
    """Расшифровывает текст, зашифрованный шифром Виженера."""
    clean_key = _clean_key(key)
    if not clean_key:
        return "Ошибка: ключ должен содержать буквы русского алфавита"

    result = ""
    key_index = 0

    for char in text:

        if char in RUS_ALPHABET:
            pos = _find_pos(RUS_ALPHABET, char)
            key_pos = _find_pos(RUS_ALPHABET, clean_key[key_index])

            result += RUS_ALPHABET[(pos - key_pos) % ALPHABET_LENGTH]
            key_index = (key_index + 1) % len(clean_key)

        elif char in RUS_ALPHABET_UPPER:
            pos = _find_pos(RUS_ALPHABET_UPPER, char)
            key_pos = _find_pos(RUS_ALPHABET, clean_key[key_index])

            result += RUS_ALPHABET_UPPER[(pos - key_pos) % ALPHABET_LENGTH]
            key_index = (key_index + 1) % len(clean_key)

        else:
            result += char

    return result


def read_key_from_file(filename: str | Path) -> str:
    """Читает ключ из файла."""
    path = Path(filename)
    with path.open("r", encoding="utf-8") as file:
        key = file.read().strip()
        if not key:
            raise ValueError("Файл с ключом пуст")
        return key