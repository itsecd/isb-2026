import math
from scipy.special import erfc, gammaincc
import constants


def read_sequence(filename):
    """Чтение последовательности из файла"""
    try:
        with open(filename, 'r') as f:
            data = f.read().strip()
        data = ''.join([c for c in data if c in '01'])
        return [int(bit) for bit in data]
    except FileNotFoundError:
        return None


def frequency_test(sequence):
    """Частотный побитовый тест"""
    n = len(sequence)
    x = [1 if bit == 1 else -1 for bit in sequence]
    s_n = abs(sum(x)) / math.sqrt(n)
    return erfc(s_n / math.sqrt(2))


def runs_test(sequence):
    """Тест на одинаковые подряд идущие биты"""
    n = len(sequence)
    pi = sum(sequence) / n
    
    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    
    v_n = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            v_n += 1
    
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    if denominator == 0:
        return 0.0
    
    return erfc(abs(v_n - 2 * n * pi * (1 - pi)) / denominator)


def longest_run_test(sequence):
    """Тест на самую длинную последовательность единиц в блоке"""
    n = len(sequence)
    M = constants.BLOCK_SIZE
    K = 3
    N_blocks = n // M
    pi = constants.PI_VALUES
    v = [0, 0, 0, 0]
    
    for i in range(N_blocks):
        block = sequence[i * M:(i + 1) * M]
        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1
    
    chi_square = 0
    for i in range(K + 1):
        expected = N_blocks * pi[i]
        if expected > 0:
            chi_square += ((v[i] - expected) ** 2) / expected
    
    return gammaincc(K / 2, chi_square / 2)


def save_results():
    """Сохранение результатов тестирования"""
    with open(constants.RESULTS_FILENAME, 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ NIST\n")
        f.write("="*50 + "\n\n")
        
        for filename, description in constants.TEST_FILES:
            sequence = read_sequence(filename)
            if not sequence or len(sequence) < constants.SEQUENCE_LENGTH:
                continue
                
            sequence = sequence[:constants.SEQUENCE_LENGTH]
            
            p_freq = frequency_test(sequence)
            p_runs = runs_test(sequence)
            p_long = longest_run_test(sequence)
            
            f.write(f"{description}:\n")
            f.write(f"  Частотный тест: {p_freq:.6f}\n")
            f.write(f"  Тест на серии: {p_runs:.6f}\n")
            f.write(f"  Тест на длинные серии: {p_long:.6f}\n\n")
            
            ones = sum(sequence)
            f.write(f"  Статистика: 1={ones}, 0={constants.SEQUENCE_LENGTH-ones}\n")
            f.write("-"*40 + "\n\n")


if __name__ == "__main__":
    save_results()
