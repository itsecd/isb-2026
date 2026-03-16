import random

def main():
    seq = ''.join(str(random.randint(0, 1)) for _ in range(128))
    
    with open("generator/python.txt", "w") as f:
        f.write(seq)
    
    print("Python: python.txt")

if __name__ == "__main__":
    main()