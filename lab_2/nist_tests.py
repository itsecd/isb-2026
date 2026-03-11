import math
from typing import List, Tuple
from scipy.special import gammaincc


def read_sequence(path: str) -> str:
    """Read binary sequence from file"""
    with open(path, encoding="utf-8") as file:
        return file.read().strip()


def frequency_test(bits: str) -> float:
    """Frequency Test"""
    n = len(bits)
    s = sum(1 if bit == "1" else -1 for bit in bits)
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value


def runs_test(bits: str) -> float:
    """Runs Test"""
    eps = [int(bit) for bit in bits]
    zeta = sum(eps)/len(bits)
    if (abs(zeta - 0.5) > 2/math.sqrt(len(bits))):
        return 0.0
    V_n = 0
    for i in range (len(bits)-1):
        if eps[i] != eps[i+1]:
            V_n +=1
    p_value = math.erfc(abs(V_n - 2* len(bits)*zeta*(1-zeta))/(2*math.sqrt(2*len(bits))*zeta*(1-zeta)))
    return p_value


def longest_run_test(bits: str) -> float:
    """Longest Run of Ones Test"""
    block_size = 8
    num_blocks = len(bits) // block_size
    counts = [0, 0, 0, 0]

    for i in range(num_blocks):
        block = bits[i * block_size:(i + 1) * block_size]
        longest = 0
        current = 0
        for bit in block:
            if bit == "1":
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        if longest <= 1:
            counts[0] += 1
        elif longest == 2:
            counts[1] += 1
        elif longest == 3:
            counts[2] += 1
        else:
            counts[3] += 1

    probabilities = [0.2148, 0.3672, 0.2305, 0.1875]
    chi_square = sum(((counts[i] - num_blocks * probabilities[i]) ** 2) / (num_blocks * probabilities[i]) for i in range(4))
    df = 3
    p_value = gammaincc(df / 2, chi_square / 2)
    return p_value


def status(p_value: float) -> str:
    """Return 'Passed' or 'Failed' based on p-value"""
    if p_value >= 0.01:
        return "Passed"
    else:
        return "Failed"


def compile_analysis(bits: str, language: str) -> (str, str):
    """Return console string with P-values and file string with Passed/Failed"""
    p_freq = frequency_test(bits)
    p_runs = runs_test(bits)
    p_long = longest_run_test(bits)

    str = (
        f"\nFor {language}:\n"
        f"Frequency test: {p_freq} ({status(p_freq)})\n"
        f"Runs test: {p_runs} ({status(p_runs)})\n"
        f"Longest run test: {p_long} ({status(p_long)})\n"
    )

    return str


if __name__ == "__main__":
    python_seq = ("Python", "sequences/seq_python.txt")
    java_seq = ("Java", "sequences/seq_java.txt")
    cpp_seq = ("C++", "sequences/seq_cpp.txt")

    res = "\n"

    res += compile_analysis(read_sequence(python_seq[1]), python_seq[0])
    res += compile_analysis(read_sequence(java_seq[1]), java_seq[0])
    res += compile_analysis(read_sequence(cpp_seq[1]), cpp_seq[0])

    print(res)

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(res)

    print("Results saved to result.txt")