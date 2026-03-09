"""Простой генератор псевдослучайной последовательности на Python
Использует стандартный ГПСЧ Python (random)"""

import random
import os

def main():    
    random.seed()
    
    # Генерируем 128 бит
    sequence = ""
    for i in range(128):
        sequence = sequence + str(random.randint(0, 1))
    
    print(sequence)
    
    # Создаем папку sequences, если её нет
    if not os.path.exists("sequences"):
        os.makedirs("sequences")
        print("Создана папка: sequences")
    
    # Сохранение в файл
    try:
        with open("sequences/sequence_python.txt", "w") as file:
            file.write(sequence)
        print("Последовательность сохранена в файл: sequences/sequence_python.txt")
    except Exception as e:
        print("Ошибка при сохранении в файл:", e)
    

if __name__ == "__main__":
    main()