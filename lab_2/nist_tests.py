import math
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


def runs_test(bits: str):
    """Runs Test"""
    n = len(bits)

    pi = bits.count("1") / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return "Test isn't working"

    runs = 1

    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1

    numerator = abs(runs - (2 * n * pi * (1 - pi)))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    p_value = math.erfc(numerator / denominator)

    return p_value
    

def longest_run_test(bits: str) -> Tuple[float, float, List[int]]:
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

    chi_square = 0

    for i in range(4):
        expected = num_blocks * probabilities[i]
        chi_square += ((counts[i] - expected) ** 2) / expected

    df = 3

    p_value = gammaincc(df / 2, chi_square / 2)

    return p_value


def compile_analysis(bits: str, language: str) -> str:
    """Run tests and return formatted result"""
    p_value_freq = frequency_test(bits)
    p_value_runs = runs_test(bits)
    p_value_long = longest_run_test(bits)

    result = (
        f"\nFor {language}:\n"
        f"Frequency test P-value: {p_value_freq}\n"
        f"Runs test P-value: {p_value_runs}\n"
        f"Longest run test P-value: {p_value_long}\n"
    )

    return result


if __name__ == "__main__":

    python_bits = read_sequence("sequences/seq_python.txt")
    java_bits = read_sequence("sequences/seq_java.txt")
    cpp_bits = read_sequence("sequences/seq_cpp.txt")

    results = ""
    results += compile_analysis(python_bits, "Python")
    results += compile_analysis(java_bits, "Java")
    results += compile_analysis(cpp_bits, "C++")

    print(results)

    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(results)

    print("Results saved to result.txt")