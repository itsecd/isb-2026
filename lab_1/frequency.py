from collections import Counter


def analyze(text):
    """Проводит частотный анализ текста"""
    total_chars = len(text)
    counter = Counter(text)
    sorted_freq = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    frequencies = [(char, count, count/total_chars) for char, count in sorted_freq]
    return frequencies

def print_table(frequencies):
    """Выводит таблицу частот"""
    print("\nЧастотный анализ текста:")
    print("Символ | Кол-во | Частота")
    for char, count, freq in frequencies:
        if char == ' ':
            display = '(пробел)'
        elif char == '\n':
            display = '(перенос)'
        else:
            display = char
        print(f"  {display:6} | {count:6} | {freq:.6f}")