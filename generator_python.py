import random
import constants

def generate_sequence(filename, length):
    """Генерация псевдослучайной последовательности"""
    with open(filename, 'w') as f:
        for _ in range(length):
            f.write(str(random.randint(0, 1)))

if __name__ == "__main__":
    generate_sequence("sequence_python.txt", constants.SEQUENCE_LENGTH)