import os


def load_text_from_file(file_path: str) -> str:
    """Функция для загрузки текста из файла
    на вход принимает путь к файлу с зашифрованным текстом
    возвращает содержимое файла в виде строки
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def count_characters(text: str) -> tuple:
    """Функция для подсчета количества каждого символа в тексте
    на вход принимает строку текста
    возвращает словарь с подсчетом символов и общее количество символов
    """
    char_count = {}
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1
    
    total_chars = len(text)
    return char_count, total_chars


def calculate_probabilities(char_count: dict, total_chars: int) -> list:
    """Функция для расчета вероятностей появления символов
    на вход принимает словарь с подсчетом символов и общее количество символов
    возвращает отсортированный по убыванию вероятности список символов с их данными
    """
    sorted_by_prob = sorted(
        char_count.items(), 
        key=lambda x: x[1] / total_chars, 
        reverse=True
    )
    return sorted_by_prob


def format_frequency_table(sorted_data: list, total_chars: int, unique_chars: int) -> list:
    """Функция для форматирования таблицы частотности
    на вход принимает отсортированные данные, общее количество символов и количество уникальных символов
    возвращает список строк для записи в файл
    """
    output = []
    output.append(f"Общее количество символов: {total_chars}")
    output.append(f"Уникальных символов: {unique_chars}")
    output.append("\n\nСортировка по убыванию вероятности:")
    output.append("Символ | Количество | Вероятность")
    output.append("-" * 40)
    
    for char, count in sorted_data:
        probability = count / total_chars
        display_char = char
        output.append(f"'{display_char}' : {count:6d} | {probability:.6f}")
    
    return output


def save_results_to_file(output_lines: list, output_path: str) -> None:
    """Функция для сохранения результатов в файл
    на вход принимает список строк для записи и путь к выходному файлу
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))


def main() -> None:
    """Основная функция для запуска анализа частотности символов"""
    os.chdir('task2')
    
    # Загрузка текста из файла
    text = load_text_from_file('shifred_text.txt')
    
    # Подсчет символов
    char_count, total_chars = count_characters(text)
    
    # Расчет вероятностей и сортировка
    sorted_data = calculate_probabilities(char_count, total_chars)
    
    # Форматирование таблицы
    output_lines = format_frequency_table(sorted_data, total_chars, len(char_count))
    
    # Сохранение результатов
    save_results_to_file(output_lines, 'frequency_table.txt')
    
    print("\n" + "=" * 50)
    print("Результаты сохранены в файл frequency_table.txt")
    print("=" * 50)


if __name__ == "__main__":
    main()