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


