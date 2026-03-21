import math
import os.path

from scipy.special import gammaincc


def frequency_test(binary: str) -> float:
    """
    Frequency monobit test.
    Used to evaluate the randomness of binary sequences.
    :param binary: binary sequences to check.
    :return: evaluated P-value.
    """
    n = len(binary)
    n_sum = sum(1 if b == '1' else -1 for b in binary)
    s_n = abs(n_sum) / math.sqrt(n)
    p_value = math.erfc(s_n / math.sqrt(2))
    return p_value


def runs_test(binary: str) -> float:
    """
    Runs test.
    The purpose of the runs test is to determine whether the number of runs
    of ones and zeros of various lengths is as expected for a random sequence.
    :param binary: binary sequences to check.
    :return: evaluated P-value.
    """
    n = len(binary)
    zeta = binary.count('1') / n

    if abs(zeta - 0.5) >= (2 / math.sqrt(n)):
        return 0.0

    v_n = 1
    for i in range(n - 1):
        if binary[i] != binary[i + 1]:
            v_n += 1

    p_value = math.erfc(abs(v_n - 2 * n * zeta * (1 - zeta)) / (2 * math.sqrt(2 * n) * zeta * (1 - zeta)))
    return p_value


def longest_run_ones_in_block_test(binary: str) -> float:
    """
    Test for the Longest Run of Ones in a Block.
    The purpose of this test is to determine whether the length of the longest
    run of ones within the tested sequence is consistent with the length of
    the longest run of ones that would be expected in a random sequence.
    :param binary: binary sequences to check.
    :return: evaluated P-value.
    """
    n = len(binary)
    m = 8

    pi_probs = [0.2148, 0.3672, 0.2305, 0.1875]
    v_values = [0, 0, 0, 0]

    blocks = [binary[i:i + m] for i in range(0, n, m)]

    for block in blocks:
        max_sequence = max(len(run) for run in block.split('0'))

        if max_sequence <= 1:
            v_values[0] += 1
        elif max_sequence == 2:
            v_values[1] += 1
        elif max_sequence == 3:
            v_values[2] += 1
        else:
            v_values[3] += 1

    chi_sq = 0.0
    for i in range(4):
        chi_sq += ((v_values[i] - 16 * pi_probs[i]) ** 2) / (16 * pi_probs[i])

    p_value = gammaincc(1.5, chi_sq / 2)
    return p_value


def run_tests_for_sequence(sequence: str, name: str) -> str:
    """
    Run all 3 tests for sequence.
    :param sequence: binary sequences to check.
    :param name: name of sequence generator for display purpose.
    """
    result_txt = f"Analyze {name} sequence: {sequence}\n"

    p1 = frequency_test(sequence)
    p2 = runs_test(sequence)
    p3 = longest_run_ones_in_block_test(sequence)

    result_txt += f"1. Frequency (Monobit) Test. P-value: {p1}  -  {'success' if p1 >= 0.01 else 'fail'}\n"
    result_txt += f"2. Runs test. P-value: {p2}  -  {'success' if p2 >= 0.01 else 'fail'}\n"
    result_txt += f"3. Test for the Longest Run of Ones in a Block. P-value: {p3}  -  {'success' if p3 >= 0.01 else 'fail'}\n"

    return result_txt


def main() -> None:
    """
    Main function
    """
    sequences = {
        "CPP": "cpp_random.txt",
        "Java": "java_random.txt"
    }

    output = "results.txt"
    results = ""

    for name, file in sequences.items():
        if os.path.exists(file):
            with open(file, 'r') as f:
                sequence = f.read().strip()
                if len(sequence) == 128:
                    test_output = run_tests_for_sequence(sequence, name)
                    print(test_output)
                    results += test_output
                else:
                    err = f"Sequence must contain 128 bit.\n"
                    print(err)
                    results += err
        else:
            err = f"File with sequence not found: {file}\n"
            print(err)
            results += err

    try:
        with open(output, 'w') as o:
            o.write(results)
        print(f"Results saved at {output}")
    except Exception as e:
        print(f"Can't write result in file: {output}. Error: {e}")


if __name__ == "__main__":
    main()
