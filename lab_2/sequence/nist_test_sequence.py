import math
import os


def load_sequence(file_path: str) -> str:
    """Open file with sequences and cleaning spaces"""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r') as f:
        return f.read().strip()

def frequency_test(sequence: str) -> str:
    """Frequency test function"""

    n: int = len(sequence)
    s_n: int = 0
    for bit in sequence:
        if bit == '1':
            s_n += 1
        else:
            s_n -= 1

    s_obs: float = abs(s_n) / math.sqrt(n)
    res: str = f"Test - 1: Frequency \n"
    res += f"Sum (S_n): {s_n}\n"
    res += f"Stastics (S_obs): {s_obs:.4f}\n"
    res += "P-value: erfc(S_obs / sqrt(2))\n"
    return res

def runs_test(sequence: str) -> str:
    """Runs test"""
    n: int = len(sequence)
    ones_count: int = sequence.count('1')
    pi: float = ones_count / n

    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return("Test failed")

    v_n = 1
    for i in range(n - 1):
        if sequence[i] != sequence[i+1]:
            v_n += 1

    numerator: float = abs(v_n - 2 * n * pi * (1 - pi))
    denominator: float = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    s_obs: float = numerator / denominator
    res: str = f"Test - 2: Runs \n"
    res += f"V_n: {v_n}\n"
    res += f"S_obs: {s_obs:.4f}\n"
    return res

def longest_run_test(sequence: str) -> str:
    """Longest run test funcion XD"""

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
    res = f"Test - 3: Longest runs\n"
    res += f"[<=1, 2, 3, >=4]: {v}\n"
    res += f"Chi-squeare: {x2_obs:.4f}"
    return res

def run_full_tests():
    base_path = "../generate/results/"
    targets = {
            "C++": "cpp_result",
            "Python": "python_result",
            "Java": "java_result"
    }

    report_lines = []

    for lang, filename in targets.items():
        full_path = os.path.join(base_path, filename)
        seq = load_sequence(full_path)
        
        header = f"\n{'='*10} Analysis {lang} ({filename}) {'='*10}\n"
        print(header)
        report_lines.append(header)
        
        if not seq:
            msg = f"Error file {filename} not found.\n"
            print(msg)
            report_lines.append(msg)
            continue

        results = [
            frequency_test(seq),
            runs_test(seq),
            longest_run_test(seq)
        ]
        
        for r in results:
            print(r)
            report_lines.append(r)

    with open("nist_report.txt", "w", encoding="utf-8") as f:
        f.writelines(report_lines)
    print("\n[OK] Results sace in nist_report.txt")


if __name__ == "__main__":
    run_full_tests()
