import random


def writeFile(sequence: list[int]) -> None:
    '''
    Writes the sequence to a file.
    '''
    with open("lab_2/python_sequence.txt", "w", encoding = "utf-8") as file:
        for number in sequence:
            file.write(str(number))
    
    return None


def createRandomSequence() -> None:
    '''
    Сreates a pseudo-random sequence of numbers.
    '''
    sequence = []
    size = 128

    for i in range(size):
        sequence.append(random.randint(0, 1))

    try:
        writeFile(sequence)
    except Exception as e:
        print(f"Error: {e}")

    return None


if __name__ == "__main__":
    createRandomSequence()
