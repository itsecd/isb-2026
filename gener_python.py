import random

def gener():
    result = []
    for _ in range(128):
        a = random.randint(0, 1)
        result.append(str(a))
    return ''.join(result)

def save(filename, sequence):
    with open(filename, "w") as f:
        f.write(sequence)

def main():
    seq = gener()
    print(seq)
    save("seq_py.txt", seq)

if __name__ == "__main__":
    main()