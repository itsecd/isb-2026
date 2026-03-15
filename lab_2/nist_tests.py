import math
import scipy.special

class NISTTests:

    @staticmethod
    def frequency_test(sequence):
        """
        Частотный побитовый тест (Frequency (Monobit) Test).
        """
        n = len(sequence)
        # Преобразуем '0' -> -1, '1' -> 1
        x = [1 if bit == '1' else -1 for bit in sequence]
        s_n = abs(sum(x)) / math.sqrt(n)
        # Дополнительная функция ошибок: erfc(x) = 1 - erf(x)
        p_value = math.erfc(s_n / math.sqrt(2))
        return p_value

    @staticmethod
    def runs_test(sequence):
        """
        Тест на одинаковые подряд идущие биты (Runs Test).
        """
        n = len(sequence)
        pi = sequence.count('1') / n

        tau = 2 / math.sqrt(n)
        # Предварительное условие на частоту единиц
        if abs(pi - 0.5) >= tau:
            return 0.0

        v_n = 1
        for i in range(1, n):
            if sequence[i] != sequence[i-1]:
                v_n += 1

        p_value = math.erfc(abs(v_n - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))
        return p_value

    @staticmethod
    def longest_run_ones_in_block_test(sequence):
        """
        Тест на самую длинную последовательность единиц в блоке
        (Test for the Longest Run of Ones in a Block).
        Специализированная версия для N=128, M=8.
        """
        n = len(sequence)
        if n != 128:
            raise ValueError("Этот тест настроен для последовательности длиной 128 бит.")

        m = 8
        k = 3  # Количество категорий (v0, v1, v2, v3)
        num_blocks = n // m

        # Теоретические вероятности Pi для M=8
        pi_values = [0.2148, 0.3672, 0.2305, 0.1875]

        v = [0, 0, 0, 0]

        for i in range(num_blocks):
            block = sequence[i*m:(i+1)*m]
            max_run = 0
            current_run = 0
            for bit in block:
                if bit == '1':
                    current_run += 1
                    max_run = max(max_run, current_run)
                else:
                    current_run = 0
            # Классифицируем блок на основе max_run
            if max_run <= 1:
                v[0] += 1
            elif max_run == 2:
                v[1] += 1
            elif max_run == 3:
                v[2] += 1
            else:  # max_run >= 4
                v[3] += 1

        # Вычисляем Хи-квадрат
        chi_squared = 0
        for i in range(4):
            expected = num_blocks * pi_values[i]
            chi_squared += ((v[i] - expected) ** 2) / expected

        # Вычисляем P-значение с помощью неполной гамма-функции (igamc)
        # gammaincc(a, x) = 1 / Gamma(a) * integral from x to inf of t^(a-1) * e^(-t) dt
        p_value = scipy.special.gammaincc(k / 2, chi_squared / 2)
        return p_value


if __name__ == "__main__":
    # Последовательность, сгенерированная на C++ для примера
    seq_cpp = "10100110101110011100010101101101100010001101111000111010010101110100110111001100111010110100101000110110111000110101110010110001"
    # Убираем пробелы, если они есть
    seq_cpp = seq_cpp.replace(" ", "")

    print("Анализ последовательности (C++):")
    print(f"Последовательность: {seq_cpp}")

    p_freq = NISTTests.frequency_test(seq_cpp)
    p_runs = NISTTests.runs_test(seq_cpp)
    p_long = NISTTests.longest_run_ones_in_block_test(seq_cpp)

    print(f"\nРезультаты тестов (P-значения):")
    print(f"1. Частотный побитовый тест: {p_freq:.6f}")
    print(f"2. Тест на одинаковые подряд идущие биты: {p_runs:.6f}")
    print(f"3. Тест на самую длинную последовательность единиц в блоке: {p_long:.6f}")

    print(f"\nВыводы (критерий P-значение >= 0.01):")
    print(f"1. {'Случайная' if p_freq >= 0.01 else 'Неслучайная'}")
    print(f"2. {'Случайная' if p_runs >= 0.01 else 'Неслучайная'}")
    print(f"3. {'Случайная' if p_long >= 0.01 else 'Неслучайная'}")