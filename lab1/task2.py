import os
from collections import Counter
from typing import Dict, List, Tuple, Optional
from lab1.constants import (
    ENCODED_FILE,
    FREQ_TABLE_FILE,
    DECRYPTED_RESULT_FILE,
    FINAL_DECODED_FILE,
    FINAL_KEY_FILE
)

class FrequencyAnalyzer:
    """Класс для частотного анализа зашифрованного текста и подстановки
    предположительных расшифровок на основе введённых пользователем замен."""
    def __init__(self) -> None:
        """Инициализация анализатора с алфавитом (заглавные буквы + пробел)."""
        self.alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

    def analyze(self, text: str) -> List[Tuple[str, int]]:
        """Выполняет частотный анализ текста и сохраняет таблицу частот в файл."""
        counter = Counter(text)
        # Сохраняем таблицу частот
        try:
            with open('lab1/data/task2_freq_table.txt', 'w', encoding='utf-8') as f:
                total_chars = sum(counter.values())
                f.write("Символ | Частота\n")
                f.write("-" * 20 + "\n")
                for char, count in counter.most_common():
                    if char != '\n':
                        f.write(f"  {char:4} | {count/total_chars:.6f}\n")
        except IOError as e:
            print(f"Ошибка при записи таблицы частот: {e}")
        
        return counter.most_common()

    def apply_guesses(self, text: str, user_guesses: Dict[str, str]) -> str:
        """Применяет к тексту частичную подстановку на основе словаря предположений.
        Символы, для которых нет предположения, заменяются на '*'."""
        current_map = {}
        for char in set(text):
            if char != '\n':
                current_map[char] = user_guesses.get(char, '*') 
        
        mapping = str.maketrans(current_map)
        return text.translate(mapping)
    
    def save_intermediate_result(self, text: str) -> None:
        """Сохраняет текущий результат дешифровки в промежуточный файл."""
        try:
            with open(DECRYPTED_RESULT_FILE, 'w', encoding='utf-8') as f:
                f.write(text)
        except IOError as e:
            print(f"Ошибка при сохранении промежуточного результата: {e}")

    def save_final_results(self, decoded_text: str, key_dict: Dict[str, str]) -> None:
        """Сохраняет окончательную расшифровку и подобранный ключ."""
        try:
            with open(FINAL_DECODED_FILE, 'w', encoding='utf-8') as f:
                f.write(decoded_text)
        except IOError as e:
            print(f"Ошибка при сохранении окончательной расшифровки: {e}")

        try:
            with open(FINAL_KEY_FILE, 'w', encoding='utf-8') as f:
                for cipher_char, plain_char in key_dict.items():
                    f.write(f"{cipher_char} -> {plain_char}\n")
        except IOError as e:
            print(f"Ошибка при сохранении ключа: {e}")

def main() -> None:
    """Основная функция для вызова методов"""
    analyzer = FrequencyAnalyzer()
    
     # Чтение зашифрованного текста
    try:
        with open(ENCODED_FILE, 'r', encoding='utf-8') as f:
            encoded_text = f.read()
    except FileNotFoundError:
        print(f"Файл {ENCODED_FILE} не найден. Создайте его с шифротекстом!")
        return
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Генерируем таблицу частот
    analyzer.analyze(encoded_text)
    print(f"Таблица частот сохранена в {FREQ_TABLE_FILE}")

    # Начальное предположение (можно задать через константу или оставить так)
    user_guesses: Dict[str, str] = {'2': ' '}

    while True:
        decrypted_text = analyzer.apply_guesses(encoded_text, user_guesses)
        analyzer.save_intermediate_result(decrypted_text)
        print(f"Текущий результат сохранён в {DECRYPTED_RESULT_FILE}")
        print("Текущие известные символы:", user_guesses)

        user_input = input("Введите замену (например, Я=О) или 'exit' для завершения: ")

        if user_input.lower() == 'exit':
            break

        if '=' in user_input:
            parts = user_input.split('=')
            if len(parts) == 2:
                cipher_char = parts[0].strip()
                plain_char = parts[1].strip().upper()
                user_guesses[cipher_char] = plain_char
                continue

        print("\n[!] Ошибка ввода. Используйте формат СИМВОЛ=БУКВА.")

    # Сохраняем итоговые результаты
    analyzer.save_final_results(decrypted_text, user_guesses)
    print("\nДешифровка завершена. Результаты и ключ сохранены в папке data/")


if __name__ == "__main__":
    main()