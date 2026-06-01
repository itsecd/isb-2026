#!/usr/bin/env python3
# lab_2/src/tests/run_all.py
"""
Точка входа для запуска всех тестов NIST
"""

import sys
from pathlib import Path

# Добавляем путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from nist_runner import (
    get_data_dir,
    load_sequence,
    run_tests_on_sequence,
    save_results_csv,
    print_summary,
)


def main() -> int:
    """Главная функция"""
    print("\n" + "=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №2: ТЕСТЫ NIST")
    print("Статистический анализ псевдослучайных последовательностей")
    print("=" * 70)
    
    data_dir = get_data_dir()
    sequences_dir = data_dir / "sequences"
    
    # Список последовательностей для тестирования
    # Формат: (имя_файла, название_источника)
    sequences = [
        ("cpp_sequence.txt", "C++"),
        ("java_sequence.txt", "Java"),
        ("python_sequence.txt", "Python"),
    ]
    
    all_results = []
    
    print(f"\n📁 Папка с данными: {data_dir}")
    print(f"🔍 Тестируем последовательности из: {sequences_dir}\n")
    
    for filename, source_name in sequences:
        filepath = sequences_dir / filename
        
        print(f"\n{'─' * 70}")
        print(f"🧪 Тестирование: {source_name} ({filename})")
        print(f"{'─' * 70}")
        
        if not filepath.exists():
            print(f"⚠️  Файл не найден: {filepath}")
            print(f"   Запустите генераторы в lab_2/src/generators/")
            continue
        
        # Загрузка последовательности
        sequence = load_sequence(str(filepath))
        
        if not sequence:
            print(f"⚠️  Пустая или невалидная последовательность")
            continue
        
        print(f"📊 Длина: {len(sequence)} бит")
        print(f"📊 Единиц: {sequence.count('1')}, Нулей: {sequence.count('0')}")
        print(f"\n🔬 Результаты тестов:")
        
        # Запуск тестов
        results = run_tests_on_sequence(sequence, source_name)
        all_results.extend(results)
    
    # Сохранение результатов
    if all_results:
        csv_path = save_results_csv(all_results)
        print(f"\n💾 Результаты сохранены: {csv_path}")
        
        # Сводка
        print_summary(all_results)
        
        # Общий вывод
        print("\n📋 ВЫВОД:")
        print("   • P-value ≥ 0.01 → последовательность считается случайной")
        print("   • P-value < 0.01 → отклоняем гипотезу о случайности")
        print("   • Для криптографии рекомендуется P-value ближе к 1.0")
    
    print("\n" + "=" * 70)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())