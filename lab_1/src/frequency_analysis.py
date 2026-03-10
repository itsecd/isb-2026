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
    Возвращает отсортированный список кортежей (символ, количество) и общее число символов.
    """
    cnt = Counter(text)
    total = sum(cnt.values())
    freq = sorted(cnt.items(), key=lambda x: x[1], reverse=True)
    return freq, total


def print_frequency_report(freq, total):
    """Выводит отчёт по частотам в консоль"""
    print(f"\nВсего символов: {total}")
    print(f"Уникальных символов: {len(freq)}\n")
    print(f"{'№':<3} | {'Символ':<10} | {'Кол-во':<8} | {'%':<7}")
    print("-" * 50)

    for i, (ch, count) in enumerate(freq):
        pct = count / total * 100
        ch_display = "[ПРОБЕЛ]" if ch == " " else ch
        print(f"{i + 1:<3} | {ch_display:<10} | {count:<8} | {pct:<7.1f}")


def save_frequency_report(freq, total, filename="task2_frequencies.txt"):
    """Сохраняет отчёт по частотам в файл"""
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, filename)

    content = "ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА\n" + "=" * 60 + "\n\n"
    content += f"Всего символов: {total}\nУникальных символов: {len(freq)}\n\n"
    content += f"{'Символ':<12} | {'Кол-во':<10} | {'Частота (%)':<12}\n"
    content += "-" * 60 + "\n"

    for i, (ch, count)