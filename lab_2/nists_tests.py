import os
import math

from scipy.special import gammaincc
from conf import BLOCK_LENGTH, PI, DIRECTORY, PVALUE, OUTPUT


def readFromFile(filePath: str) -> str:
    """ Read from file """
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            data = f.read().strip()
            return data

    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] => file: \"{filePath}\" not found")

    except Exception as e:
        raise Exception(f"[ERROR] => something went wrong: {e}")


def writeToFile(filePath: str, mode: str, data: str) -> None:
    """ Write to file """
    try:
        with open(filePath, mode, encoding='utf-8') as f:
            f.write(data)

    except Exception as e:
        raise Exception(f"[ERROR] => something went wrong: {e}")


def frequencyTest(sequence: str) -> float:
    """ frequency test """
    S = sequence.count("1") - sequence.count("0")
    S *= 1 / (len(sequence)) ** 0.5

    return math.erfc(abs(S) / math.sqrt(2))


def identicalBitsTest(sequence: str) -> float:
    """ identical bits test """
    eps = sequence.count("1") / len(sequence)
    if not (abs(eps - 0.5) < 2 / (len(sequence)) ** 0.5):
        return 0
    
    V = sequence.count("01") + sequence.count("10")
    num = abs(V - 2 * len(sequence) * eps * (1 - eps))
    denom = 2 * ((2 * len(sequence)) ** 0.5) * eps * (1 - eps)

    return math.erfc(num / denom)


def longestTest(sequence: str) -> float:
    """ longest sequence test """
    v = [0, 0, 0, 0]

    for i in range(len(sequence) // BLOCK_LENGTH):
        block = sequence[i * BLOCK_LENGTH:(i + 1) * BLOCK_LENGTH]
        if (block.count("1111") > 0):
            v[3] += 1
        elif (block.count("111") > 0):
            v[2] += 1
        elif (block.count("11") > 0):
            v[1] += 1
        else:
            v[0] += 1

    Xi = 0
    for i in range(4):
        Xi += ((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i])

    return gammaincc(1.5, Xi / 2)

def main() -> None:
    """Main function."""
    files = os.listdir(DIRECTORY)
    results = []

    for file in files:
        if ".txt" in file and file.lower() != "cmakelists.txt":
            sequence = readFromFile(DIRECTORY + file)
            results.append([file, frequencyTest(sequence), identicalBitsTest(sequence), longestTest(sequence)])

    for result in results:
        result.append("True" if all(x >= PVALUE for x in result[1:]) else "False")

    writeToFile(OUTPUT, "w", "Programming language | Frequency test | Sequence identical test | Longest sequence test | Results\n\n")
    for result in results:
        writeToFile(OUTPUT, "a", " | ".join(str(x) for x in result) + "\n")

    print("[RUN] => success completed!")


if __name__ == "__main__":
    main()