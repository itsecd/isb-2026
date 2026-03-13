import subprocess
import os

def generate_cpp_sequences():
    """Компиляция и запуск C++ генератора"""
    subprocess.run(['g++', '-o', 'generator_cpp', 'generator.cpp'])
    subprocess.run(['./generator_cpp'])
    print()

def generate_java_sequences():
    """Компиляция и запуск Java генератора"""
    subprocess.run(['javac', 'Generator.java'])
    subprocess.run(['java', 'Generator'])
    print()

def read_sequences_from_file(filename):
    """Чтение последовательностей из файла"""
    sequences = []
    with open(filename, 'r') as f:
        for line in f:
            if ':' in line:
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    seq = parts[1].strip()
                    if all(c in '01' for c in seq):
                        sequences.append(seq)
    return sequences

def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №2")
    print()
    
    generate_cpp_sequences()
    generate_java_sequences()
    
    sequences_cpp = read_sequences_from_file('sequences_cpp.txt')
    sequences_java = read_sequences_from_file('sequences_java.txt')
    
    all_sequences = sequences_cpp + sequences_java
    
    print(f"Всего последовательностей для тестирования: {len(all_sequences)}")
    print()
    
    from nist import run_all_tests
    run_all_tests(all_sequences, 'final_test_results.txt')
    
    print("Результаты сохранены в:")
    print("  - sequences_cpp.txt")
    print("  - sequences_java.txt")
    print("  - final_test_results.txt")

if __name__ == "__main__":
    main()