import math

def load_bits(path):
    with open(path, "r") as f:
        return f.read().strip()


def frequency_test(bits):
    n = len(bits)
    s = sum(1 if b == '1' else -1 for b in bits)
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value


def runs_test(bits):
    n = len(bits)
    pi = bits.count('1') / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            v += 1

    p_value = math.erfc(
        abs(v - 2 * n * pi * (1 - pi)) /
        (2 * math.sqrt(2 * n) * pi * (1 - pi))
    )

    return p_value


def longest_run_test(bits, block_size=128):
    n = len(bits)
    N = n // block_size

    longest_runs = []

    for i in range(N):
        block = bits[i * block_size:(i + 1) * block_size]

        max_run = 0
        current_run = 0

        for b in block:
            if b == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        longest_runs.append(max_run)

    average = sum(longest_runs) / len(longest_runs)
    return average


def run_tests(file, out):
    bits = load_bits(file)

    freq = frequency_test(bits)
    runs = runs_test(bits)
    longest = longest_run_test(bits)

    result = (
        f"File: {file}\n"
        f"Frequency test p-value: {freq}\n"
        f"Runs test p-value: {runs}\n"
        f"Longest run average: {longest}\n"
        + "-" * 40 + "\n"
    )

    print(result)

    with open(out, "a") as f:
        f.write(result)


if __name__ == "__main__":

    files = [
        "bits_cpp.txt",
        "bits_python.txt",
        "bits_java.txt"
    ]

    output_file = "test_results.txt"

    for f in files:
        run_tests(f, output_file)