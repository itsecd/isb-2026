import random

def main():
    """
    Основная функция генератора.
    Генерирует бинарную последовательность длиной 128 бит с фиксированным зерном (42)
    и сохраняет её в файл 'seq_python.txt'.
    """
    random.seed(42)
    seq = ''.join(str(random.randint(0, 1)) for _ in range(128))
    print(seq)
    with open('seq_python.txt', 'w') as f:
        f.write(seq)

if __name__ == "__main__":
    main()