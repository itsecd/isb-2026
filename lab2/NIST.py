from math import sqrt, erfc
from scipy.special import gammaincc
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", default="input.txt")
    parser.add_argument("-o", "--output", help="output file", default="output.txt")
    return parser.parse_args()

def read_file(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()

def write_file(filename: str, data: list[str]) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(data)

def frequency_test(seq: str) -> float:
    count = 0
    for bit in seq:
        if bit == "1":
            count += 1
        else:
            count -= 1
    s = abs(count) / sqrt(len(seq))
    p = erfc(s / sqrt(2))
    return p

def runs_test(seq: str) -> float:
    count = 0
    for bit in seq:
        count += int(bit)
    ratio: float = count / len(seq)
    if abs(ratio - 0.5) >= 2 / sqrt(len(seq)):
        return 0.0
    v = 1
    for i in range(len(seq) - 1):
        if seq[i] != seq[i + 1]:
            v += 1
    p = erfc(abs(v - 2 * len(seq) * ratio * (1 - ratio)) / (2 * sqrt(2 * len(seq)) * ratio * (1 - ratio)))
    return p

def longest_ones_test(seq: str) -> float:
    v_n = [0, 0, 0, 0]
    for i in range(16):
        block = seq[i * 8:(i + 1) * 8]
        longest = 0
        cur = 0
        for char in block:
            if char == "1":
                cur += 1
                if cur > longest:
                    longest = cur
            else:
                cur = 0
        if longest <= 1:
            v_n[0] += 1
        elif longest == 2:
            v_n[1] += 1
        elif longest == 3:
            v_n[2] += 1
        else:
            v_n[3] += 1

    pi_n = [0.2148, 0.3672, 0.2305, 0.1875]
    x = 0
    for i in range(4):
        x += ((v_n[i] - 16 * pi_n[i]) ** 2) / (16 * pi_n[i])
    return gammaincc(1.5, x / 2)

def main():
    args = parse_args()
    #args.input = "C:\\Users\\mrsmi\\Documents\\GitHub\\isb-2026\\lab2\\cppseq.txt"
    #args.output = "C:\\Users\\mrsmi\\Documents\\GitHub\\isb-2026\\lab2\\cppoutput.txt"
    sequences = read_file(args.input)
    output = list()
    for seq in sequences:
        output.append(str(frequency_test(seq)) + "\n")
        output.append(str(runs_test(seq)) + "\n")
        output.append(str(longest_ones_test(seq)) + "\n")
    write_file(args.output, output)

if __name__ == "__main__":
    main()