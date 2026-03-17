import os
from collections import Counter


def get_data_dir():
    """Определяет путь к папке data относительно расположения скрипта"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, "data")


def analyze_frequency(text):
    """
    Подсчитывает частоту символов в тексте.
    Возвращает отсортированный список кортежей (символ, частота_в_процентах) 
    и общее число символов.
    """
    cnt = Counter(text)
    total = sum(cnt.values())
    
    # Вычисляем частоту в процентах для каждого символа
    freq = [(char, (count / total) * 100) for char, count in cnt.items()]
    
    # Сортируем по убыванию частоты
    freq = sorted(freq, key=lambda x: x[1], reverse=True)
    
    return freq, total


def print_frequency_report(freq, total):
    """Выводит отчёт по частотам в консоль"""
    print(f"\nВсего символов: {total}")
    print(f"Уникальных символов: {len(freq)}\n")
    print(f"{'№':<3} | {'Символ':<10} | {'Частота (%)':<12}")
    print("-" * 50)

    for i, (ch, frequency) in enumerate(freq):
        ch_display = "[ПРОБЕЛ]" if ch == " " else ch
        print(f"{i + 1:<3} | {ch_display:<10} | {frequency:<12.2f}")


def save_frequency_report(freq, total, filename="task2_frequencies.txt"):
    """Сохраняет отчёт по частотам в файл"""
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, filename)

    content = "ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА\n" + "=" * 60 + "\n\n"
    content += f"Всего символов: {total}\nУникальных символов: {len(freq)}\n\n"
    content += f"{'Символ':<12} | {'Частота (%)':<12}\n"
    content += "-" * 60 + "\n"

    for i, (ch, frequency) in enumerate(freq):
        ch_display = "[ПРОБЕЛ]" if ch == " " else ch
        content += f"{ch_display:<12} | {frequency:<12.2f}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path


def run_frequency_analysis(text, filename="task2_frequencies.txt"):
    """
    Главная функция: выполняет анализ, выводит в консоль и сохраняет в файл.
    Возвращает кортеж (freq, total).
    """
    freq, total = analyze_frequency(text)
    print_frequency_report(freq, total)
    path = save_frequency_report(freq, total, filename)
    print(f"\n✅ Частоты сохранены: {path}")
    return freq, total