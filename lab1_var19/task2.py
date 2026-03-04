import os
from typing import Dict, List, Tuple
from collections import Counter
from constants import (
    TASK2_ORIGINAL_FILE, TASK2_FREQUENCIES_FILE,
    TASK2_DECRYPTED_FILE, TASK2_KEY_FILE,
    RUSSIAN_FREQUENCIES_SORTED
)


def read_encrypted_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def calculate_frequencies(text: str) -> List[Tuple[str, float]]:
    total_chars = len(text)
    char_counts = Counter(text)
    frequencies = [(char, count / total_chars)
                   for char, count in char_counts.items()]
    frequencies.sort(key=lambda x: x[1], reverse=True)
    return frequencies


def save_frequencies(frequencies: List[Tuple[str, float]], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Таблица частот символов в зашифрованном тексте\n")
        f.write("Символ | Частота\n")
        f.write("-" * 30 + "\n")
        for char, freq in frequencies:
            f.write(f"{char:5} | {freq:.6f}\n")


def create_initial_mapping(
    encrypted_freq: List[Tuple[str, float]],
    russian_freq: List[Tuple[str, float]]
) -> Dict[str, str]:
    mapping = {}
    for (enc_char, _), (rus_char, _) in zip(encrypted_freq, russian_freq):
        mapping[enc_char] = rus_char
    return mapping


def apply_mapping(text: str, mapping: Dict[str, str]) -> str:
    result = []
    for char in text:
        if char in mapping:
            result.append(mapping[char])
        else:
            result.append(char)
    return "".join(result)


def save_key(mapping: Dict[str, str], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Найденный ключ шифрования (зашифрованный -> исходный):\n")
        f.write("-" * 50 + "\n")
        for enc_char in sorted(mapping.keys()):
            f.write(f"{enc_char} -> {mapping[enc_char]}\n")


def interactive_refine(mapping: Dict[str, str], encrypted_text: str) -> Dict[str, str]:
    refined = mapping.copy()

    while True:
        current_text = apply_mapping(encrypted_text, refined)
        print("\n" + "="*80)
        print("ТЕКСТ С ТЕКУЩИМ СОПОСТАВЛЕНИЕМ:")
        print("="*80)
        print(current_text)
        print("="*80)

        print("\nТЕКУЩИЙ КЛЮЧ (зашифрованный -> исходный):")
        for enc_char in sorted(refined.keys()):
            print(f"{enc_char} -> {refined[enc_char]}", end="  ")
        print("\n")

        print("ДЕЙСТВИЯ:")
        print("1 - Заменить один символ")
        print("2 - Поменять местами два символа")
        print("3 - Сохранить и выйти")
        print("4 - Выйти без сохранения")

        choice = input("\nВыберите действие: ").strip()

        if choice == '1':
            enc_char = input(
                "Введите символ из зашифрованного текста: ").strip()
            if enc_char not in refined:
                print("Такого символа нет в ключе!")
                continue

            print(f"Текущее соответствие: {enc_char} -> {refined[enc_char]}")
            new_value = input(
                "Введите новое значение (русскую букву или пробел): ").strip()

            if len(new_value) == 1:
                refined[enc_char] = new_value
                print("Сопоставление обновлено")

        elif choice == '2':
            char1 = input("Введите первый символ: ").strip()
            char2 = input("Введите второй символ: ").strip()

            if char1 in refined and char2 in refined:
                refined[char1], refined[char2] = refined[char2], refined[char1]
                print("Символы поменяны местами")
            else:
                print("Один из символов не найден в ключе!")

        elif choice == '3':
            print("Сохранение и выход...")
            return refined

        elif choice == '4':
            print("Выход без сохранения...")
            break

        else:
            print("Неверный выбор, попробуйте снова")

    return refined


def decrypt_task2() -> None:
    print("Задание 2")
    print("Дешифровка текста методом частотного анализа\n")

    os.makedirs("task2", exist_ok=True)

    encrypted_text = read_encrypted_file(TASK2_ORIGINAL_FILE)
    print(
        f"Зашифрованный текст прочитан, длина: {len(encrypted_text)} символов")

    frequencies = calculate_frequencies(encrypted_text)
    save_frequencies(frequencies, TASK2_FREQUENCIES_FILE)
    print(f"Таблица частот сохранена в: {TASK2_FREQUENCIES_FILE}")

    print("\nТоп-10 символов в зашифрованном тексте:")
    for i, (char, freq) in enumerate(frequencies[:10], 1):
        print(f"{i:2}. '{char}' : {freq:.6f}")

    print("\nТоп-10 символов в русском языке (с пробелом):")
    for i, (char, freq) in enumerate(RUSSIAN_FREQUENCIES_SORTED[:10], 1):
        print(f"{i:2}. '{char}' : {freq:.6f}")

    mapping = create_initial_mapping(frequencies, RUSSIAN_FREQUENCIES_SORTED)

    print("\nНачальное сопоставление создано.")
    print("Запуск интерактивного уточнения...")

    final_mapping = interactive_refine(mapping, encrypted_text)

    decrypted_text = apply_mapping(encrypted_text, final_mapping)

    with open(TASK2_DECRYPTED_FILE, "w", encoding="utf-8") as f:
        f.write(decrypted_text)

    save_key(final_mapping, TASK2_KEY_FILE)

    print(f"\nДешифрованный текст сохранен в: {TASK2_DECRYPTED_FILE}")
    print(f"Найденный ключ сохранен в: {TASK2_KEY_FILE}")

    print("\nДешифрованный текст:")
    print("-"*50)
    print(decrypted_text)
    print("-"*50)


if __name__ == "__main__":
    decrypt_task2()
