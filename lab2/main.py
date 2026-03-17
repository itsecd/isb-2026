import os
from utils import read_sequence, save_result
from tests.frequency_test import frequency_test, print_frequency_test
from tests.runs_test import runs_test, print_runs_test
from tests.longest_run_test import longest_run_test, print_longest_run_test

def main():
    # Создаём папку для результатов
    os.makedirs("results", exist_ok=True)
    
    # Очищаем файл с результатами
    with open("results/test_results.txt", 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ СЛУЧАЙНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ\n")
        f.write("="*60 + "\n\n")
    
    # ТРИ файла - по одному от каждого языка
    sequences = [
        ("sequences/cpp_sequence.txt", "C++ (MT)"),
        ("sequences/java_sequence.txt", "Java (Random)"),
        ("sequences/python_sequence.txt", "Python (random)"),
    ]
    
    # Тестируем каждую последовательность
    for seq_file, seq_name in sequences:
        if not os.path.exists(seq_file):
            print(f" Файл {seq_file} не найден, пропускаем...")
            continue
        
        print("\n" + "="*60)
        print(f"ТЕСТИРОВАНИЕ: {seq_name}")
        print("="*60)
        
        sequence = read_sequence(seq_file)
        if not sequence:
            continue
        
        print(f"Длина: {len(sequence)} бит")
        print(f"Первые 50 бит: {sequence[:50]}...")
        
        # Три теста для каждой последовательности
        p1, r1 = frequency_test(sequence)
        save_result("test_results.txt", seq_name, "Частотный побитовый тест", p1, r1)
        
        p2, r2 = runs_test(sequence)
        save_result("test_results.txt", seq_name, "Тест на одинаковые подряд идущие биты", p2, r2)
        
        # longest_run_test возвращает 3 значения
        p3, r3, v = longest_run_test(sequence)
        save_result("test_results.txt", seq_name, "Тест на самую длинную последовательность единиц", p3, r3)
        
        # Краткий итог
        print(f"\n📊 ИТОГ ДЛЯ {seq_name}:")
        print(f"   Частотный тест: {'' if r1 else ''} (p={p1:.4f})")
        print(f"   Тест на серии: {'' if r2 else ''} (p={p2:.4f})")
        print(f"   Тест на макс. последовательность: {'' if r3 else ''} (p={p3:.4f})")
        print(f"   Распределение длин: {v}")
    
    print("\n" + "="*60)
    print(" ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print(" Результаты сохранены в results/test_results.txt")

if __name__ == "__main__":
    main()