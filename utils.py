# utils.py
"""
Вспомогательные функции для лабораторной работы №1
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

def clean_text(text):
    text = text.upper()
    cleaned = []
    for char in text:
        if char in RUS_ALPHABET:
            cleaned.append(char)
        elif char == '\n':
            cleaned.append(' ')
    return ''.join(cleaned)

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return None

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def calculate_frequencies(text):
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

def print_frequencies(freq_dict, title="Таблица частот"):
    print(f"\n{title}:")
    print("-" * 40)
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    for char, freq in sorted_items[:15]:
        print(f"  {char if char != ' ' else 'ПРОБЕЛ'}: {freq:.6f}")
    print("-" * 40)