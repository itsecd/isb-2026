"""
Утилиты для лабораторной работы №1
Содержит общие функции для работы с текстом и частотным анализом
"""

RUS_ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
ALPHABET_LEN = len(RUS_ALPHABET)

REFERENCE_FREQUENCIES = {
    ' ': 0.128675, 'О': 0.096456, 'И': 0.075312, 'Е': 0.072292,
    'А': 0.064841, 'Н': 0.061820, 'Т': 0.061619, 'С': 0.051953,
    'Р': 0.040677, 'В': 0.039267, 'М': 0.029803, 'Л': 0.029400,
    'Д': 0.026983, 'П': 0.026379, 'К': 0.025977, 'У': 0.013290,
    'Ч': 0.011679, 'Ж': 0.010673, 'Г': 0.009867, 'Х': 0.008659,
    'Ф': 0.007249, 'Й': 0.006847, 'Ю': 0.006847, 'Б': 0.006645,
    'Ц': 0.005034, 'Ш': 0.004229, 'Щ': 0.003625, 'Э': 0.002416,
    'Ъ': 0.000000, 'Ы': 0.015707, 'Ь': 0.015103
}

REFERENCE_SORTED = [char for char, _ in sorted(
    REFERENCE_FREQUENCIES.items(), 
    key=lambda x: x[1], 
    reverse=True
)]

def clean_text(text: str) -> str:
    """
    Очищает текст от лишних символов.
    
    Args:
        text: Входной текст
        
    Returns:
        Только буквы русского алфавита и пробелы в верхнем регистре
    """
    text = text.upper()
    cleaned = []
    for char in text:
        if char in RUS_ALPHABET:
            cleaned.append(char)
        elif char == '\n':
            cleaned.append(' ')
    return ''.join(cleaned)

def read_file(filename: str) -> str | None:
    """
    Безопасное чтение файла.
    
    Args:
        filename: Путь к файлу
        
    Returns:
        Содержимое файла или None если файл не найден
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return None

def write_file(filename: str, content: str) -> None:
    """
    Запись содержимого в файл.
    
    Args:
        filename: Путь к файлу
        content: Содержимое для записи
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def calculate_frequencies(text: str) -> tuple[dict, list]:
    """
    Подсчет частот символов в тексте.
    
    Args:
        text: Входной текст
        
    Returns:
        (словарь частот, список символов по убыванию частоты)
    """
    total_chars = len(text)
    freq = {}
    
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    for char in freq:
        freq[char] = freq[char] / total_chars
    
    sorted_chars = [char for char, _ in sorted(
        freq.items(), 
        key=lambda x: x[1], 
        reverse=True
    )]
    
    return freq, sorted_chars

def print_frequencies(freq_dict: dict, title: str = "Таблица частот") -> None:
    """
    Вывод таблицы частот в консоль.
    
    Args:
        freq_dict: Словарь частот
        title: Заголовок таблицы
    """
    print(f"\n{title}:")
    print("-" * 50)
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    for i, (char, freq) in enumerate(sorted_items[:15], 1):
        display_char = 'ПРОБЕЛ' if char == ' ' else char
        print(f"  {i:2}. {display_char:6}: {freq:.6f} ({freq*100:.2f}%)")
    print("-" * 50)