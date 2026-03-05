import math
import os

from scipy.special import gammaincc

from consts import BLOCK_SIZE, PI, DIRECTORY, PVALUE, OUTPUT


def test_frequency(text: str) -> float:
    """
    Frequency NIST test.
    Return P value for this text
    """
    Sn = text.count("1") - text.count("0")
    Sn *= 1 / (len(text)) ** 0.5

    return math.erfc(Sn / 2 ** 0.5)


def test_identical_bits(text: str) -> float:
    """
    NIST test for a sequence of identical bits.
    Return P value for this text
    """
    ksi = text.count("1") / len(text)
    if not (abs(ksi - 0.5) < 2 / (len(text)) ** 0.5):
        return 0
    Vn = text.count("01") + text.count("10")
    num = abs(Vn - 2 * len(text) * ksi * (1 - ksi))
    denom = 2 * ((2 * len(text)) ** 0.5) * ksi * (1 - ksi)
    return math.erfc(num / denom)


def test_longest_sequence(text: str) -> float:
    """
    NIST test for the longest sequence of ones in a block.
    Return P value for this text
    """
    v = [0, 0, 0, 0]

    for i in range(len(text) // BLOCK_SIZE):
        block = text[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
        if (block.count("1111") > 0):
            v[3] += 1
        elif (block.count("111") > 0):
            v[2] += 1
        elif (block.count("11") > 0):
            v[1] += 1
        else:
            v[0] += 1

    xi = 0
    for i in range(4):
        xi += ((v[i] - 16 * PI[i]) ** 2) / (16 * PI[i])

    return gammaincc(1.5, xi / 2)


def read(filename: str) -> str:
    """Read file from filename. Return str readed text"""
    try:
        with open(filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        exit(-1)


def main() -> None:
    """Main function."""
    files = os.listdir(DIRECTORY)
    results = []
    for file in files:
        if ".txt" in file and file.lower() != "cmakelists.txt":
            text = read(DIRECTORY + file)
            results.append([file, test_frequency(text), test_identical_bits(text), test_longest_sequence(text)])

    for arr in results:
        arr.append("True" if all(x >= PVALUE for x in arr[1:]) else "False")

    with open(OUTPUT, "w") as f:
        f.write("Language | Frequency test | test sequence of identical bits | test longest sequence | Results\n\n")
        for arr in results:
            for i in arr:
                f.write(str(i))
                f.write(" ")
            f.write("\n")


if __name__ == "__main__":
    main()
