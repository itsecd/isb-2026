# lab_2/src/tests/nist_runner.py
"""
Модуль для запуска тестов NIST и сохранения результатов
"""

import csv
import os
import sys
from pathlib import Path
from typing import List, Dict

# Добавляем текущую папку в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from nist_core import NISTTests


def get_data_dir() -> Path:
    """Возвращает путь к папке data/ относительно этого скрипта"""
    script_dir = Path(__file__).parent.parent.parent
    return script_dir / "data"


def load_sequence(filepath: str) -> str:
    """
    Загружает бинарную последовательность из файла
    
    :param filepath: путь к файлу (относительный или абсолютный)
    :return: строка из '0' и '1' или пустая строка при ошибке
    """
    try:
        # Преобразуем в абсолютный путь относительно data/
        if not Path(filepath).is_absolute():
            filepath = get_data_dir() / "sequences" / filepath
        
        with open(filepath, 'r', encoding='utf-8') as f:
            sequence = f.read().strip()
        
        # Валидация: только '0' и '1'
        if not all(c in '01' for c in sequence):
            print(f"⚠️  Warning: {filepath} contains non-binary data", file=sys.stderr)
            return ''.join(c for c in sequence if c in '01')
        
        return sequence
    
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}", file=sys.stderr)
        return ""


def run_tests_on_sequence(sequence: str, source_name: str) -> List[Dict]:
    """
    Запускает все три теста NIST на последовательности
    
    :param sequence: бинарная строка
    :param source_name: название источника (C++, Java, Python)
    :return: список словарей с результатами
    """
    results = []
    
    if len(sequence) == 0:
        return [{
            "Source": source_name,
            "Test": "SEQUENCE_EMPTY",
            "P-Value": "N/A",
            "Result": "FAIL"
        }]
    
    tests = [
        ("Monobit Frequency", NISTTests.monobit_test),
        ("Runs Test", NISTTests.runs_test),
        ("Longest Run of Ones", NISTTests.longest_run_ones_test),
    ]
    
    for test_name, test_func in tests:
        try:
            p_value = test_func(sequence)
            status = "PASS" if p_value >= NISTTests.ALPHA else "FAIL"
            
            results.append({
                "Source": source_name,
                "Test": test_name,
                "P-Value": f"{p_value:.6f}",
                "Result": status,
            })
            
            # Вывод в консоль
            emoji = "✅" if status == "PASS" else "❌"
            print(f"  {emoji} {test_name:<25} P={p_value:.6f} [{status}]")
            
        except Exception as e:
            print(f"  ❌ {test_name} ERROR: {e}", file=sys.stderr)
            results.append({
                "Source": source_name,
                "Test": test_name,
                "P-Value": "ERROR",
                "Result": "FAIL",
            })
    
    return results


def save_results_csv(results: List[Dict], filename: str = "nist_results.csv") -> str:
    """
    Сохраняет результаты в CSV файл
    
    :param results: список словарей с результатами
    :param filename: имя файла
    :return: путь к сохранённому файлу
    """
    output_path = get_data_dir() / "results" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = ["Source", "Test", "P-Value", "Result"]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    return str(output_path)


def print_summary(results: List[Dict]):
    """Выводит сводку по результатам"""
    print("\n" + "=" * 70)
    print("СВОДКА ПО РЕЗУЛЬТАТАМ")
    print("=" * 70)
    
    # Группируем по источнику
    by_source = {}
    for r in results:
        src = r["Source"]
        if src not in by_source:
            by_source[src] = {"pass": 0, "fail": 0, "total": 0}
        
        by_source[src]["total"] += 1
        if r["Result"] == "PASS":
            by_source[src]["pass"] += 1
        else:
            by_source[src]["fail"] += 1
    
    for source, stats in by_source.items():
        emoji = "✅" if stats["fail"] == 0 else "⚠️"
        print(f"{emoji} {source}: {stats['pass']}/{stats['total']} тестов пройдено")
    
    print("=" * 70)