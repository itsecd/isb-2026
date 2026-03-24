import math
from scipy.special import gammaincc

def read_sequence_from_file(filename):
    """
    Читает двоичную последовательность из текстового файла.

    Параметры:
    filename (str): Имя файла, содержащего последовательность из символов '0' и '1'.

    Возвращает:
    str: Строка, состоящая только из символов '0' и '1'.

    Исключения:
    ValueError: Если в файле присутствуют символы, отличные от '0', '1' или пробельных.
    """
    with open(filename, 'r') as f:
        content = f.read()
    seq = ''.join(content.split())
    if not all(c in '01' for c in seq):
        raise ValueError(f"Файл {filename} содержит недопустимые символы (допустимы только 0 и 1)")
    return seq

def frequency_test(seq):
    """
    Частотный побитовый тест (Frequency Test).

    Оценивает, насколько доля единиц в последовательности близка к 1/2.
    Возвращает P-значение, вычисленное с использованием функции ошибок.

    Параметры:
    seq (str): Двоичная последовательность в виде строки.

    Возвращает:
    float: P-значение теста.
    """
    n = len(seq)
    x = [1 if b == '1' else -1 for b in seq]
    s_n = sum(x) / math.sqrt(n)
    p_value = math.erfc(abs(s_n) / math.sqrt(2))
    return p_value

def runs_test(seq):
    """
    Тест на одинаковые подряд идущие биты (Runs Test).

    Проверяет, соответствует ли количество серий (последовательностей одинаковых битов)
    ожидаемому для случайной последовательности.

    Параметры:
    seq (str): Двоичная последовательность в виде строки.

    Возвращает:
    float: P-значение теста. Если доля единиц слишком далека от 0.5, возвращает 0.0.
    """
    n = len(seq)
    ones = seq.count('1')
    z = ones / n

    if abs(z - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0

    v_n = 0
    for i in range(n - 1):
        if seq[i] != seq[i + 1]:
            v_n += 1
    numerator = abs(v_n - 2 * n * z * (1 - z))
    denominator = 2 * math.sqrt(2 * n) * z * (1 - z)
    p_value = math.erfc(numerator / denominator)
    return p_value

def longest_run_ones_in_block_test(seq):
    """
    Тест на самую длинную последовательность единиц в блоке (для длины 128 бит).

    Последовательность разбивается на блоки по 8 бит. Для каждого блока определяется
    максимальная длина серии единиц. Затем вычисляется статистика хи-квадрат и P-значение.

    Параметры:
    seq (str): Двоичная последовательность длиной ровно 128 бит.

    Возвращает:
    float: P-значение теста.

    Исключения:
    ValueError: Если длина последовательности не равна 128.
    """
    n = len(seq)
    if n != 128:
        raise ValueError("Данный тест разработан только для последовательностей длиной 128 бит")

    m = 8
    num_blocks = n // m

    v = [0, 0, 0, 0]
    for i in range(num_blocks):
        block = seq[i * m:(i + 1) * m]
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
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

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    chi_square = 0.0
    for i in range(4):
        expected = num_blocks * pi[i]
        chi_square += (v[i] - expected) ** 2 / expected

    p_value = gammaincc(3.0 / 2, chi_square / 2)
    return p_value

def analyze_file(input_filename, output_filename):
    """
    Анализирует файл с двоичной последовательностью и записывает результаты в выходной файл.

    Выполняет три теста: частотный, runs и длинной серии единиц. Выводит результаты на экран
    и сохраняет их в текстовый файл. В случае ошибки записывает сообщение об ошибке.

    Параметры:
    input_filename (str): Имя входного файла с двоичной последовательностью.
    output_filename (str): Имя файла для сохранения результатов.
    """
    try:
        seq = read_sequence_from_file(input_filename)
        
        lines = []
        lines.append(f"Анализ файла: {input_filename}")
        lines.append(f"Длина последовательности: {len(seq)}")
        lines.append(f"Последовательность: {seq} ")
        lines.append("")

        p_freq = frequency_test(seq)
        p_runs = runs_test(seq)
        p_long = longest_run_ones_in_block_test(seq)

        lines.append(f"Частотный тест:                 P = {p_freq:.6f}  {'+' if p_freq >= 0.01 else '-'}")
        lines.append(f"Тест на одинаковые биты (Runs): P = {p_runs:.6f}  {'+' if p_runs >= 0.01 else '-'}")
        lines.append(f"Тест на длинную серию единиц:   P = {p_long:.6f}  {'+' if p_long >= 0.01 else '-'}")
        lines.append("")

        if p_freq >= 0.01 and p_runs >= 0.01 and p_long >= 0.01:
            lines.append("ВЫВОД: последовательность признаётся случайной по всем трём тестам.")
        else:
            lines.append("ВЫВОД: последовательность НЕ признаётся случайной (не прошла один или несколько тестов).")

        for line in lines:
            print(line)

        with open(output_filename, 'a', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n\n')

        print(f"Результаты сохранены в файл: {output_filename}\n")

    except Exception as e:
        error_msg = f"Ошибка при обработке файла {input_filename}: {e}"
        print(error_msg)
        with open(output_filename, 'a', encoding='utf-8') as f:
            f.write(error_msg)

if __name__ == "__main__":
    files = [
        ("generator_cpp.txt", "results.txt"),
        ("generator_java.txt", "results.txt")
    ]
    for in_fname, out_fname in files:
        analyze_file(in_fname, out_fname)