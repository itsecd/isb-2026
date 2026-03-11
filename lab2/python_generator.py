import random

def main():
    sequence = ''
    for _ in range(128):
        sequence += str(random.randint(0, 1))
    
    print("Python последовательность (128 бит):")
    print(sequence)
    
    with open('sequence_python.txt', 'w') as f:
        f.write(sequence)
    
    print("Сохранено в sequence_python.txt")

if __name__ == "__main__":
    random.seed()
    main()