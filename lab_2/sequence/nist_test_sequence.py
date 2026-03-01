import math


def frequency_test(sequence: str):
    """Frequency test function"""

    n: int = len(sequence)

    s_n: int = 0
    for bit in sequence:
        if bit == '1':
            s_n += 1
        else:
            s_n -= 1

    s_obs: float = abs(s_n) / math.sqrt(n)

    print(f"Sum (S_n): {s_n}")
    print(f"Stastics (S_obs): {s_obs:.4f}")
    print("erfc(S_obs / sqrt(2)) = ... (online calc ;( )")
    return s_obs

def runs_test(sequence: str):
    """Runs test"""
    n: int = len(sequence)
    ones_count: int = sequence.count('1')
    pi: float = ones_count / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        print("Test failed")
        return 0

    v_n = 1
    for i in range(n - 1):
        if sequence[i] != sequence[i+1]:
            v_n += 1

    numerator: float = abs(v_n - 2 * n * pi * (1 - pi))
    denominator: float = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    s_obs: float = numerator / denominator

    print(f"V_n: {v_n}")
    print(f"S_obs: {s_obs:.4f}")
    return s_obs

def longest_run_test(sequence: str):
    """"""

    n: int = len(sequence)
    m = 8
    n_blocks = 16
    v = [0, 0, 0, 0]

    for i in range(n_blocks):
        block = sequence[i*m : (i+1)*m]
        max_run = max(len(s) for s in block.split('0'))

        if max_run <=1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    x2_obs = 0 
    for i in range(4):
        x2_obs += ((v[i] - n_blocks * pi[i])**2) / (n_blocks * pi[i])

    print("[<=1, 2, 3, >=4]: {v}")
    print("chi_square: {x2_obs:.4f}")
    print("Calc: df=3")
    return x2_obs

frequency_test("10110101110111001000000101110100101001110000000100100010011000000101011000000001101011101010011111010110001101111101001110100100")
runs_test("10110101110111001000000101110100101001110000000100100010011000000101011000000001101011101010011111010110001101111101001110100100")
longest_run_test("10110101110111001000000101110100101001110000000100100010011000000101011000000001101011101010011111010110001101111101001110100100")
