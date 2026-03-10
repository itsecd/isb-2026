import math


def readFile(filename: str) -> list[int]:
    '''
    Reads a number sequence from a file.
    '''
    sequence = []
    
    with open(filename, "r", encoding = "utf-8") as file:
        data = file.read()
        for number in data:
            sequence.append(int(number))

    return sequence
    

def main():
    python_seq = readFile("lab_2/python_sequence.txt")
    print(python_seq)
    pass


if __name__ == "__main__":
    main()