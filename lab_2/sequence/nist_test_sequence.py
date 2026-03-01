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


