
import subprocess
import os
from nist_tests import NISTTests

def generate_cpp_sequences():
    """Компиляция и запуск C++ генератора"""
    print("Generating C++ sequences...")
    subprocess.run(['g++', '-o', 'random_cpp', 'random_generator_cpp.cpp', '-std=c++11'])
    subprocess.run(['./random_cpp'])
    print()

def generate_java_sequences():
    """Компиляция и запуск Java генератора"""
    print("Generating Java sequences...")
    subprocess.run(['javac', 'RandomGeneratorJava.java'])
    subprocess.run(['java', 'RandomGeneratorJava'])
    print()

def read_sequences_from_file(filename):
    """Чтение последовательностей из файла"""
    sequences = {}
    try:
        with open(filename, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
            current_name = None
            for line in lines:
                if line.startswith('Sequence'):
                    if ':' in line:
                        current_name = line.split(':')[0].strip()
                elif line.strip() and len(line.strip()) == 128 and all(c in '01' for c in line.strip()):
                    if current_name:
                        sequences[current_name] = line.strip()
    except FileNotFoundError:
        print(f"File {filename} not found")
    
    return sequences
def main():
    print("LABORATORY WORK #2")
    print("Statistical Analysis of Pseudorandom Sequences")
    print("STEP 1: Generating pseudorandom sequences")
    
    try:
        generate_cpp_sequences()
    except Exception as e:
        print(f"C++ generation error: {e}")
    
    try:
        generate_java_sequences()
    except Exception as e:
        print(f"Java generation error: {e}")
    
    sequences = {}
    
    cpp_seqs = read_sequences_from_file('sequences_cpp.txt')
    sequences.update(cpp_seqs)
    
    java_seqs = read_sequences_from_file('sequences_java.txt')
    sequences.update(java_seqs)
    
    if not sequences:
        print("Using default test sequences...")
        sequences = {
            "Test_Sequence_1": "1011001011010010110100101101001011010010110100101101001011010010110100101101001011010010110100101101001011010010",
            "Test_Sequence_2": "01101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001101001",
            "Test_Sequence_3": "1100101011001010110010101100101011001010110010101100101011001010110010101100101011001010110010101100101011001010"
        }
    
    print(f"\nLoaded {len(sequences)} sequences\n")
    
    print("\nSTEP 2: Running NIST Statistical Tests")
    
    nist = NISTTests()
    all_results = {}
    
    for name, seq in sequences.items():
        results = nist.run_all_tests(seq, name)
        all_results[name] = results
    
    with open('detailed_test_results.txt', 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ ЛАБОРАТОРНОЙ РАБОТЫ №2\n")
        
        f.write("ЧАСТЬ 1: СГЕНЕРИРОВАННЫЕ ПОСЛЕДОВАТЕЛЬНОСТИ\n")
        
        for name, seq in sequences.items():
            f.write(f"{name}:\n{seq}\n\n")
        
        f.write("\nЧАСТЬ 2: РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        
        passed_tests = 0
        total_tests = 0
        
        for name, results in all_results.items():
            f.write(f"Последовательность: {name}\n")
            f.write(f"Длина: 128 бит\n")
            
            for result in results:
                total_tests += 1
                status = "PASS" if result['passed'] else "FAIL"
                if result['passed']:
                    passed_tests += 1
                
                f.write(f"\nТест: {result['test_name']}\n")
                f.write(f"  Статистика: {result['statistic']:.6f}\n")
                f.write(f"  P-value: {result['p_value']:.6f}\n")
                f.write(f"  Результат: {status}\n")
                
                if 'observed' in result:
                    f.write(f"  Наблюдаемые значения: {result['observed']}\n")
                    f.write(f"  Ожидаемые значения: {result['expected']}\n")
            
        
        f.write("\nОБЩИЕ РЕЗУЛЬТАТЫ:\n")
        f.write(f"Всего тестов пройдено: {passed_tests}/{total_tests}\n")
        f.write(f"Процент успешных тестов: {(passed_tests/total_tests)*100:.2f}%\n")
        
        f.write("\n\nВЫВОДЫ:\n")
        
        if passed_tests == total_tests:
            f.write("Все последовательности успешно прошли все статистические тесты NIST.\n")
            f.write("Это свидетельствует о хорошем качестве генераторов псевдослучайных чисел.\n")
        else:
            f.write(f"Не все тесты были пройдены ({passed_tests}/{total_tests}).\n")
            f.write("Возможные причины:\n")
            f.write("1. Недостаточная длина последовательности (128 бит)\n")
            f.write("2. Особенности конкретных генераторов\n")
            f.write("3. Случайные флуктуации\n")
    
    print("LABORATORY WORK COMPLETED")
    print(f"\nTotal tests passed: {passed_tests}/{total_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.2f}%")
    print("\nDetailed results saved to: detailed_test_results.txt")

if __name__ == "__main__":
    main()
