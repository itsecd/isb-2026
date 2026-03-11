import math

# Частотный побитовый тест
def frequency_bit_test(sequence):
    ones = sequence.count('1')
    zeros = sequence.count('0')
    length = len(sequence)
    expected_ones = length / 2
    expected_zeros = length / 2

    result = f"Частота 1: {ones/length:.4f}, Частота 0: {zeros/length:.4f}\n"
    
    if abs(ones - expected_ones) < 0.05 * length:
        result += "Частотный тест пройден\n"
    else:
        result += "Частотный тест не пройден\n"
    
    return result

# Тест на одинаковые подряд идущие биты
def consecutive_ones_zeros(sequence):
    max_count = 0
    current_count = 1

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            current_count += 1
        else:
            if current_count > max_count:
                max_count = current_count
            current_count = 1
    if current_count > max_count:
        max_count = current_count

    result = f"Самая длинная последовательность одинаковых битов: {max_count}\n"
    
    if max_count < 6:
        result += "Тест на одинаковые биты пройден\n"
    else:
        result += "Тест на одинаковые биты не пройден\n"
    
    return result

# Тест на самую длинную последовательность единиц в блоке
def longest_run_of_ones(sequence):
    n = len(sequence)
    m = 8  # Длина блока
    num_blocks = n // m
    blocks = [sequence[i * m:(i + 1) * m] for i in range(num_blocks)]

    categories = [0, 0, 0, 0]

    for block in blocks:
        longest = 0
        current = 0

        for ch in block:
            if ch == "1":
                current += 1
                if current > longest:
                    longest = current
            else:
                current = 0

        if longest <= 1:
            categories[0] += 1
        elif longest == 2:
            categories[1] += 1
        elif longest == 3:
            categories[2] += 1
        else:
            categories[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    chi_square = 0.0
    for i in range(4):
        expected = num_blocks * pi[i]
        chi_square += ((categories[i] - expected) ** 2) / expected

    x = chi_square / 2.0
    p_value = math.erfc(math.sqrt(x)) + (2.0 / math.sqrt(math.pi)) * math.sqrt(x) * math.exp(-x)

    result = f"Тест на самую длинную последовательность единиц: p_value = {p_value}\n"
    
    if p_value >= 0.01:
        result += "Тест на самую длинную последовательность единиц пройден\n"
    else:
        result += "Тест на самую длинную последовательность единиц не пройден\n"
    
    return result

# Проверка последовательности из файла
def read_sequence(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def run_tests():
    # Чтение сгенерированной последовательности
    sequence = read_sequence('generated_sequence.txt')

    # Запуск тестов
    result = ""

    result += "\nРезультаты частотного теста:\n"
    result += frequency_bit_test(sequence)

    result += "\nРезультаты теста на одинаковые подряд идущие биты:\n"
    result += consecutive_ones_zeros(sequence)

    result += "\nРезультаты теста на самую длинную последовательность единиц в блоке:\n"
    result += longest_run_of_ones(sequence)

    # Запись результатов в файл
    with open("results.txt", "w") as f:
        f.write(result)
    
    print("Результаты тестов записаны в файл 'results.txt'.")

run_tests()