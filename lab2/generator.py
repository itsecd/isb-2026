import random
import os

def generate_bits(length):
    return ''.join(str(random.randint(0, 1)) for _ in range(length))

def main():
    # Создаём папку sequences
    os.makedirs("sequences", exist_ok=True)
    
    # Генерируем 128 бит
    bits = generate_bits(128)
    
    # Сохраняем в файл
    with open("sequences/python_sequence.txt", "w") as f:
        f.write(bits)
    
    print("Python: sequences/python_sequence.txt (128 бит)")

if __name__ == "__main__":
    main()