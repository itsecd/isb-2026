import json
import os

import constants


def read_file(file_path):
    """Чтение файла"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    

def analyze_frequencies(text):
    """Возвращает словарь частот символов, отсортированный по убыванию"""
    counts = {}

    for char in text:
        counts[char] = counts.get(char, 0) + 1

    total = len(text)
    freqs = {char: counts[char] / total for char in counts}

    return dict(
        sorted(freqs.items(), key=lambda item: item[1], reverse=True)
    )


def generate_key(encrypted_freq, reference_freq):
    """Создание ключа на основе частот"""
    key = {}
    encrypted_chars = list(encrypted_freq.keys())
    reference_chars = list(reference_freq.keys())

    for index, char in enumerate(encrypted_chars):
        if index < len(reference_chars):
            key[char] = reference_chars[index]
        else:
            key[char] = char

    return key


def apply_key(text, key):
    """Применяет ключ к тексту для получения расшифровки"""
    return "".join(key.get(char, char) for char in text)


def main():
    """Основная функция"""
    text = read_file("data/cod1.txt")

    freqs = analyze_frequencies(text)
    key = generate_key(freqs, constants.REFERENCE_FREQUENCIES)
    decrypted = apply_key(text, key)

    print("Частоты:", freqs)
    print("Сгенерированный ключ:", key)
    print("Расшифровка:", decrypted)


if __name__ == "__main__":
    main()