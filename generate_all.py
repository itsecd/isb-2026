"""Простой генератор последовательностей для тестов NIST
Запустите этот файл один раз, и он создаст все необходимые файлы"""

import random
import os

def generate_sequence():
    """Генерирует случайную последовательность из 128 бит"""
    sequence = ""
    for i in range(128):
        sequence = sequence + str(random.randint(0, 1))
    return sequence

def main():
    print("Генератор для последовательностей тестов NIST")
    
    # Создаем папку sequences
    if not os.path.exists("sequences"):
        os.makedirs("sequences")
        print("Создана папка: sequences")
    
    # Генерируем последовательность для C++
    print("\nГенерация последовательности для C++ (mt19937)...")
    seq_cpp = generate_sequence()
    
    with open("sequences/sequence_cpp.txt", "w") as f:
        f.write(seq_cpp)
    
    print(f"Последовательность: {seq_cpp[:32]}...{seq_cpp[-32:]}")
    print(f"Длина: {len(seq_cpp)} бит")
    print(f"Единиц: {seq_cpp.count('1')}, Нулей: {seq_cpp.count('0')}")
    print(f"Сохранено в: sequences/sequence_cpp.txt")
    
    # Генерируем последовательность для Java
    print("\nГенерация последовательности для Java (java.util.Random)...")
    seq_java = generate_sequence()
    
    with open("sequences/sequence_java.txt", "w") as f:
        f.write(seq_java)
    
    print(f"Последовательность: {seq_java[:32]}...{seq_java[-32:]}")
    print(f"Длина: {len(seq_java)} бит")
    print(f"Единиц: {seq_java.count('1')}, Нулей: {seq_java.count('0')}")
    print(f"Сохранено в: sequences/sequence_java.txt")
    
    # Генерируем последовательность для Python
    print("\nГенерация последовательности для Python (random)...")
    seq_python = generate_sequence()
    
    with open("sequences/sequence_python.txt", "w") as f:
        f.write(seq_python)
    
    print(f"Последовательность: {seq_python[:32]}...{seq_python[-32:]}")
    print(f"Длина: {len(seq_python)} бит")
    print(f"Единиц: {seq_python.count('1')}, Нулей: {seq_python.count('0')}")
    print(f"Сохранено в: sequences/sequence_python.txt")
    
    # Проверяем созданные файлы
    print("ПРОВЕРКА СОЗДАННЫХ ФАЙЛОВ:")
    
    cpp_size = os.path.getsize("sequences/sequence_cpp.txt")
    java_size = os.path.getsize("sequences/sequence_java.txt")
    python_size = os.path.getsize("sequences/sequence_python.txt")
    
    print(f"   sequence_cpp.txt: {cpp_size} байт")
    print(f"   sequence_java.txt: {java_size} байт")
    print(f"   sequence_python.txt: {python_size} байт")
    
    if cpp_size == 128 and java_size == 128 and python_size == 128:
        print("\nВСЕ ФАЙЛЫ СОЗДАНЫ УСПЕШНО!")
    else:
        print("\nОшибка: файлы созданы некорректно")
    

if __name__ == "__main__":
    main()