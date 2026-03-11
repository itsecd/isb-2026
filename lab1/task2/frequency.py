from collections import Counter

def analyze(text):
    """Анализ частоты символов в тексте."""
    text = text.upper()
    total = len(text)
    
    if total == 0:
        return Counter(), []
    
    counter = Counter(text)
    sorted_chars = [c for c, _ in counter.most_common()]
    return counter, sorted_chars

def make_freq_table(counter, total):
    """Формирование таблицы частот символов."""
    lines = ["ТАБЛИЦА ЧАСТОТ", "="*70]
    lines.append(f"{'Символ':^10} | {'Код':^8} | {'Кол-во':^10} | {'%':^8}")
    lines.append("-"*70)
    
    for char, count in counter.most_common():
        percent = (count / total) * 100
        display = 'пробел' if char == ' ' else char
        lines.append(f"{display:^10} | {ord(char):^8} | {count:^10} | {percent:>6.2f}%")
    
    return '\n'.join(lines)
