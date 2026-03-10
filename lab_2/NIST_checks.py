import math
from scipy.special import gammaincc


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


def frequencyMonobitTest(sequence: list[int]) -> float:
    '''
    Frequency bitwise test.
    '''
    condition = {
        1: 1,
        0: -1
    }
    sum = 0
    size = len(sequence)

    for number in sequence:
        sum += condition[number]

    S_n = abs(sum) / math.sqrt(size)
    P_value = math.erfc(S_n / math.sqrt(2))
    
    return P_value


def runsTest(sequence: list[int]) -> float:
    '''
    A test for identical consecutive bits.
    '''
    size = len(sequence)
    sum = 0
    for number in sequence:
        sum += number

    eth = sum / size
    if abs(eth - 1 / 2) >= (2 / math.sqrt(size)):
        return 0

    V_n = 0
    for i in range(size - 1):
        if  sequence[i] != sequence[i + 1]:
            V_n += 1

    numerator = abs(V_n - 2*size*eth*(1 - eth))
    denominator = 2*math.sqrt(2*size)*eth*(1 - eth)
    P_value = math.erfc(numerator / denominator)

    return P_value



def longestRunOfOnesInABlockTest(sequence: list[int]) -> float:
    '''
    A test for the longest sequence of ones in a block.
    '''
    size = len(sequence)
    block_size = 8
    blocks = []

    for i in range(0, size, block_size):
        block = sequence[i:i + block_size]
        blocks.append(block)

    v_1 = v_2 = v_3 = v_4 = 0
    for block in blocks:
        max_run = 0
        current_run = 0
        for number in block:
            if number == 1:
                current_run += 1
                max_run = max(current_run, max_run)
            else:
                current_run = 0

        if max_run <= 1:
            v_1 += 1
        elif max_run == 2:
            v_2 += 1
        elif max_run == 3:
            v_3 += 1
        else: 
            v_4 += 1

    Xi = 0
    v_i = [v_1, v_2, v_3, v_4]
    Pi_i = [0.2148, 0.3672, 0.2305, 0.1875]
    N = len(blocks)
    for i in range(len(v_i)):
        numerator = v_i[i] - N*Pi_i[i]
        denominator = N*Pi_i[i]
        Xi += pow(numerator, 2) / denominator

    P_value = gammaincc(3 / 2, Xi / 2)

    return P_value


def main():
    python_seq = readFile("lab_2/python_sequence.txt")
    python_value_1 = frequencyMonobitTest(python_seq)
    print(f"{python_value_1:.4f}")
    python_value_2 = runsTest(python_seq)
    print(f"{python_value_2:.4f}")
    python_value_3 = longestRunOfOnesInABlockTest(python_seq)
    print(f"{python_value_3:.4f}")



if __name__ == "__main__":
    main()