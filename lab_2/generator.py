import random

def main():
    random.seed(42)
    seq = ''.join(str(random.randint(0, 1)) for _ in range(128))
    
    with open('seq_python.txt', 'w') as f:
        f.write(seq)
    
    print("Последовательность сохранена в seq_python.txt")

if __name__ == "__main__":
    main()