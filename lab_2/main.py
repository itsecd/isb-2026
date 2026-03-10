import math
from scipy.special import gammaincc

ALPHA = 0.01

def read_seq(filename: str) -> str:
    
    """Читает двоичную последовательность из файла."""

    with open(filename, "r", encoding="utf-8") as f:
        seq = "".join(ch for ch in f.read() if ch in "01")
    if not seq:
        raise ValueError(f"{filename} не содержит двоичной последовательности ")
    return seq

def frequency_test(seq: str) -> dict:

    """Выполняет частотный побитовый тест."""

    n = len(seq)
    s = sum(1 if b == "1" else -1 for b in seq)
    p = math.erfc(abs(s) / math.sqrt(2 * n))
    return {"name": "Frequency Test", "p_value": p, "pass": p>=ALPHA}

def runs_test(seq: str) -> dict:

    """Выполняет тест на серии одинаковых битов."""

    n = len(seq)
    tau = seq.count("1") / n
    check = 2 / math.sqrt(n)

    if abs(tau - 0.5) >= check:
        return {"name": "Runs Test", "p_value": 0.0, "pass": False}
    
    vn = sum(1 for i in range(n - 1) if seq[i] != seq[i + 1])
    num = abs(vn - 2 * n * tau * (1 - tau))
    den = 2 * math.sqrt(2 * n) * tau * (1 - tau)
    p = math.erfc(num / den)
    return {"name": "Runs Test", "p_value": p, "pass": p >= ALPHA}

def longest_run(block: str) -> int:

    """Находит самую длинную серию единиц в блоке."""

    best = 0
    cur = 0
    for b in block:
        if b == "1":
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best

def longest_run_test(seq: str) -> dict:

    """Выполняет тест на самую длинную серию единиц в блоке."""

    M = 8

    if len(seq) != 128:
        return {"name": "Longest Run Test", "p_value": 0.0, "pass": False}
    
    probs = [0.2148, 0.3672, 0.2305, 0.1875]
    v = [0, 0, 0, 0]

    for i in range(16):
        r = longest_run(seq[i * M : (i + 1) * M])
        if r <= 1:
            v[0] += 1
        elif r == 2:
            v[1] += 1
        elif r == 3:
            v[2] += 1
        else:
            v[3] += 1
    
    chi2 = sum((v[i] - 16 * probs[i]) ** 2 / (16 * probs[i]) for i in range(4))
    p = gammaincc(3/2, chi2/2)
    return {"name": "Longest Run Test", "p_value": p, "pass": p >= ALPHA}

def run_all(filename: str) -> list[dict]:

    """Запускает все три теста для файла."""

    seq = read_seq(filename)
    return [frequency_test(seq), runs_test(seq), longest_run_test(seq)]

files = ["seq_cpp.txt", "seq_java.txt"]

with open("results.txt", "w", encoding="utf-8") as out:
    for file in files:
        try:
            results = run_all(file)
            print(f"\nФайл: {file}")
            out.write(f"\nФайл: {file}\n")

            for r in results:
                line = f"{r['name']}: p_value = {r['p_value']:.6f}, pass = {r['pass']}"
                print(line)
                out.write(line + "\n")

        except Exception as e:
            print(f"{file}: {e}")
            out.write(f"{file}: {e}\n")