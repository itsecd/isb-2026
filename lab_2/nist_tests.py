import math
from scipy.special import gammaincc
from constants import SEQ_FILES, SEQUENCE_LENGTH, BLOCK_SIZE, NUM_BLOCKS, PROBS


def frequency_test(seq: str) -> float:
    """
    Частотный побитовый тест NIST.
    
    Проверяет соотношение единиц и нулей в последовательности.
    
    Args:
        seq (str): Бинарная последовательность ('0' и '1')
        
    Returns:
        float: P-значение теста
    """
    n = len(seq)
    s = (sum(1 if bit == '1' else -1 for bit in seq))/math.sqrt(n)
    return math.erfc(abs(s) / math.sqrt(2))


def runs_test(seq: str) -> float:
    """
    Тест на переключения битов (Runs Test).
    
    Проверяет частоту переходов 0→1 и 1→0.
    
    Args:
        seq (str): Бинарная последовательность ('0' и '1')
        
    Returns:
        float: P-значение теста
    """
    n = len(seq)
    ones = seq.count('1')
    pi = ones / n
    
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0
    
    v = sum(1 for i in range(n-1) if seq[i] != seq[i+1])
    num = abs(v - 2 * n * pi * (1 - pi))
    den = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    if den == 0:
        return 0.0
    return math.erfc(num / den)


def get_blocks(seq: str, block_size: int) -> list[str]:
    """
    Разбивает последовательность на блоки.
    
    Args:
        seq (str): Бинарная последовательность
        block_size (int): Размер одного блока
        
    Returns:
        list[str]: Список блоков
    """
    blocks = []
    for i in range(0, len(seq), block_size):
        block = seq[i:i + block_size]
        blocks.append(block)
    return blocks


def max_run_in_block(block: str) -> int:
    """
    Находит самую длинную серию единиц в блоке.
    
    Args:
        block (str): Блок последовательности
        
    Returns:
        int: Длина максимальной серии единиц
    """
    max_len = 0
    current_len = 0
    for bit in block:
        if bit == '1':
            current_len += 1
            if current_len > max_len:
                max_len = current_len
        else:
            current_len = 0
    return max_len


def longest_run_test(seq: str) -> tuple[float, list[int], float]:
    """
    Тест на самую длинную серию единиц в блоке (Longest Run of Ones).
    
    Args:
        seq (str): Бинарная последовательность
        
    Returns:
        tuple[float, list[int], float]: (P-значение, статистика по блокам, хи-квадрат)
    """
    blocks = get_blocks(seq, BLOCK_SIZE)
    
    v = [0, 0, 0, 0]
    for block in blocks:
        r = max_run_in_block(block)
        if r <= 1:
            v[0] += 1
        elif r == 2:
            v[1] += 1
        elif r == 3:
            v[2] += 1
        else:
            v[3] += 1
    
    chi2 = 0
    for i in range(4):
        expected = NUM_BLOCKS * PROBS[i]
        chi2 += (v[i] - expected) ** 2 / expected
    
    p_value = gammaincc(3/2, chi2/2)
    return p_value, v, chi2


def test(seq: str, name: str) -> list[float]:
    """
    Запускает все 3 теста NIST для последовательности.
    
    Args:
        seq (str): Бинарная последовательность
        name (str): Название последовательности (для вывода)
        
    Returns:
        list[float]: Список P-значений всех тестов
    """
    print(f"\n{name}: {seq}")
    p_values = []
    
    p1 = frequency_test(seq)
    print(f"  Frequency: P={p1:.6f}")
    p_values.append(p1)
    
    p2 = runs_test(seq)
    print(f"  Runs: P={p2:.6f}")
    p_values.append(p2)
    
    p3, v, chi2 = longest_run_test(seq)
    print(f"  LongestRun: P={p3:.6f}, chi2={chi2:.4f}")
    p_values.append(p3)
    
    return p_values


def save_results(results: list[tuple[str, list[float]]]) -> None:
    """
    Сохраняет результаты тестов в файл results.txt.
    
    Args:
        results (list[tuple]): Список кортежей (название, [P-значения])
        
    Returns:
        None
    """
    test_names = ["Frequency", "Runs", "LongestRun"]
    
    with open("results.txt", "w") as f:
        f.write("NIST Test Results\n" + "=" * 50 + "\n\n")
        
        for lang, pvals in results:
            f.write(f"{lang}:\n")
            for name, p in zip(test_names, pvals):
                f.write(f"  {name}: P={p:.6f}\n")
            f.write("\n")


def main() -> None:
    """
    Основная функция: читает последовательности, запускает тесты, сохраняет результаты.
    
    Returns:
        None
    """
    print("Lab 2: NIST Tests")
    print("=" * 50)
    
    results = []
    
    for filename in SEQ_FILES:
        seq = open(filename).read().strip()
        lang = filename.split("/")[-1].replace(".txt", "")
        pvals = test(seq, lang)
        results.append((lang, pvals))
    
    save_results(results)
    print("\n" + "=" * 50)
    print("Results saved to results.txt")


if __name__ == "__main__":
    main()
