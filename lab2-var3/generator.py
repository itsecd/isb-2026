import random

def main():
    random.seed(24)
    seq = ''.join(str(random.randint(0, 1)) for _ in range(128))
    
    with open('gen_python.txt', 'w') as f:
        f.write(seq)
    
    print("Сохранено в gen_python.txt")

if __name__ == "__main__":
    main()