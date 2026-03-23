import random

def generate_sequence() -> str:
    return ''.join(str(random.randint(0, 1)) for _ in range(128))

if __name__ == '__main__':
    seq = generate_sequence()
    with open("sequence_py.txt", "w") as f:
        f.write(seq + "\n")