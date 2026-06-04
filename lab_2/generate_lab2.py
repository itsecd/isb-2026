import random

def main():
    with open("python_sequence.txt", "w") as f:
        for _ in range(128):
            f.write(str(random.randint(0, 1)))
    print("Generated python_sequence.txt")

if __name__ == "__main__":
    main()