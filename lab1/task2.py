import os
from collections import Counter

class FrequencyAnalyzer:
    def __init__(self):
        self.alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

    def analyze(self, text):
        counter = Counter(text)
        # Сохраняем таблицу частот
        with open('lab1/data/task2_freq_table.txt', 'w', encoding='utf-8') as f:
            total_chars = sum(counter.values())
            f.write("Символ | Частота\n")
            f.write("-" * 20 + "\n")
            for char, count in counter.most_common():
                if char != '\n':
                    f.write(f"  {char:4} | {count/total_chars:.6f}\n")
        
        return counter.most_common()

    def apply_guesses(self, text, user_guesses):
        current_map = {}
        for char in set(text):
            if char != '\n':
                current_map[char] = user_guesses.get(char, '*') 
        
        mapping = str.maketrans(current_map)
        return text.translate(mapping)

def main():
    analyzer = FrequencyAnalyzer()
    
    try:
        with open('lab1/data/task2_encoded.txt', 'r', encoding='utf-8') as f:
            encoded_text = f.read()
    except FileNotFoundError:
        print("Создайте файл lab1/data/task2_encoded.txt с шифротекстом!")
        return

    # Генерируем таблицу частот
    analyzer.analyze(encoded_text)
    print("Таблица частот сохранена в lab1/data/task2_freq_table.txt")

    user_guesses = {'2': ' '} 

    while True:
        decrypted_text = analyzer.apply_guesses(encoded_text, user_guesses)
        
        print("Текущий результат сохранен в файл lab1/data/decrypted_result.txt")
        with open("lab1/data/decrypted_result.txt", "w", encoding="utf-8") as file:
            file.write(decrypted_text)
        
        print("Текущие известные символы:", user_guesses)
        user_input = input("Введите замену (например, Я=О) или напишите 'exit' для сохранения: ")
        
        if user_input.lower() == 'exit':
            break
            
        if '=' in user_input:
            parts = user_input.split('=')
            if len(parts) == 2:
                cipher_char = parts[0]
                plain_char = parts[1].strip().upper()
                user_guesses[cipher_char] = plain_char
                continue
        
        print("\n[!] Ошибка ввода. Пожалуйста, используйте формат СИМВОЛ=БУКВА.")

    # Сохраняем итоговые результаты при выходе из цикла
    with open('lab1/data/task2_decoded.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
        
    with open('lab1/data/task2_key.txt', 'w', encoding='utf-8') as f:
        for cipher_char, plain_char in user_guesses.items():
            f.write(f"{cipher_char} -> {plain_char}\n")

    print("\nДешифровка завершена. Результаты и ключ сохранены в папке data/")

if __name__ == "__main__":
    main()