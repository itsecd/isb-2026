import random
import os

def read_constants():
    """Читает числа из constants.txt и возвращает список."""
    values = []
    with open('constants.txt', 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()
            if line:
                values.append(float(line))
    return values

def main():
    """Генерирует последовательность встроенным генератором Python и сохраняет в файл."""
    vals = read_constants()
    LENGTH = int(vals[0])
    
    os.makedirs('results', exist_ok=True)
    bits = ''.join(str(random.randint(0, 1)) for _ in range(LENGTH))
    
    with open('results/sequence_python.txt', 'w') as f:
        f.write(bits)

if __name__ == "__main__":
    main()