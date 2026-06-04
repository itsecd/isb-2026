import csv
import os
from nist_tests import monobit_test, runs_test, longest_run_ones_in_block

def load_sequence(filepath):
    with open(filepath, 'r') as f:
        bits = f.read().strip()
    return bits

def main():
    sequences = [
        ("C (rand)", "generators/sequences/sequence_c.txt"),
        ("C++ (mt19937)", "generators/sequences/sequence_cpp.txt"),
        ("Python (secrets)", "generators/sequences/sequence_python.txt")
    ]
    results = []
    for name, path in sequences:
        if not os.path.exists(path):
            print(f"Файл {path} не найден. Пропускаем {name}")
            continue
        bits = load_sequence(path)
        n = len(bits)
        print(f"Тестируем {name}, длина = {n} бит...")
        p_mono = monobit_test(bits)
        p_runs = runs_test(bits)
        p_long = longest_run_ones_in_block(bits)
        results.append({
            "Генератор": name,
            "Длина (бит)": n,
            "Частотный тест (p-value)": f"{p_mono:.6f}",
            "Тест прогонов (p-value)": f"{p_runs:.6f}",
            "Тест на длинную серию (p-value)": f"{p_long:.6f}" if p_long != -1 else "недостаточно данных",
            "Результат": "пройден" if (p_mono >= 0.01 and p_runs >= 0.01 and (p_long == -1 or p_long >= 0.01)) else "НЕ ПРОЙДЕН"
        })
    with open("results.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Генератор", "Длина (бит)", "Частотный тест (p-value)", 
                      "Тест прогонов (p-value)", "Тест на длинную серию (p-value)", "Результат"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print("\nРезультаты сохранены в results.csv")
    for r in results:
        print(f"{r['Генератор']}: {r['Результат']}")

if __name__ == "__main__":
    main()