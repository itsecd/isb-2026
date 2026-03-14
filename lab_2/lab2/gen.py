import random

def main():
    n = 128
    with open("seq_py.txt", "w") as f:
        for _ in range(n):
            f.write(str(random.randint(0,1)))

if __name__ == "__main__":
    main()