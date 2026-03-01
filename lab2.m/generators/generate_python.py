import random

def main():
    seq = ""
    for i in range(128):
        seq += str(random.randint(0, 1))
    
    try:
        with open("../sequences/sequence_python.txt", "w") as f:
            f.write(seq)
        print("Сохранено в ../sequences/sequence_python.txt")
    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()