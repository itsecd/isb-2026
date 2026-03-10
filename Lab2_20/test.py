'''Конечно! Вот код на языке программирования python.
 Данная программа проверяет, являются ли последовательности чисел действительно случайными.

Последовательности проходят три теста, по результатам которых, выводится вердикт, является ли последовательность случайной
Все значки из функций из сайта https://symbl.cc/ru/'''
import math
import sys

def erfc(x):
    """Дополнительная функция ошибок"""
    return math.erfc(x)

def igamc(a, x):
    """
    Неполная гамма-функция Q(a,x) для a = 3/2
    """
    if a == 1.5:
        sqrt_x = math.sqrt(x)
        return 2 * erfc(sqrt_x) + 2 * sqrt_x * math.exp(-x) / math.sqrt(math.pi)
    else:
        return 0.0

def read_sequence(filename):
    """Чтение 128-битной последовательности из файла"""
    sequence = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Пропускаем пустые строки
                if not line:
                    continue
                # Читаем все биты из строки
                for ch in line:
                    if ch in ('0', '1'):
                        sequence.append(int(ch))
        
        # Проверяем, что получили ровно 128 бит
        if len(sequence) != 128:
            print(f"ВНИМАНИЕ: Ожидалось 128 бит, получено {len(sequence)} бит")
        
        return sequence
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return None

def find_max_run(sequence):
    """
    Поиск максимальной длины подряд идущих одинаковых символов
    Возвращает (max_zeros, max_ones)
    """
    if not sequence:
        return 0, 0
    
    max_zeros = 0
    max_ones = 0
    current_zero_run = 0
    current_one_run = 0
    
    for bit in sequence:
        if bit == 0:
            current_zero_run += 1
            current_one_run = 0
            max_zeros = max(max_zeros, current_zero_run)
        else:  # bit == 1
            current_one_run += 1
            current_zero_run = 0
            max_ones = max(max_ones, current_one_run)
    
    return max_zeros, max_ones

def frequency_test(sequence):
    """
    Частотный побитовый тест (Frequency Test)
    Формула из методички:
    S_N = (1/√N) * Σ x_i, где x_i = 1 для '1', -1 для '0'
    P_value = erfc(|S_N| / √2)
    """
    n = len(sequence)
    
    # Преобразование 0 -> -1, 1 -> 1
    x = [1 if bit == 1 else -1 for bit in sequence]
    
    # Вычисление S_N = (1/√N) * Σ x_i
    s_n = sum(x) / math.sqrt(n)
    
    # Вычисление P_value = erfc(|S_N| / √2)
    p_value = erfc(abs(s_n) / math.sqrt(2))
    
    return p_value

def runs_test(sequence):
    """
    Тест на одинаковые подряд идущие биты (Runs Test)
    Формула из методички
    ζ = (1/N) * Σ ε_i
    V_N = Σ r_i, где r_i = 0 если ε_i = ε_{i+1}, 1 если ε_i ≠ ε_{i+1}
    P_value = erfc( |V_N - 2Nζ(1-ζ)| / (2√(2N) ζ(1-ζ)) )
    """
    n = len(sequence)
    
    # Вычисление ζ (доля единиц)
    pi = sum(sequence) / n
    
    # Проверка условия применимости теста |ζ - 1/2| < 2/√N
    # Для N=128: 2/√128 = 2/11.314 = 0.1768
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        print(f"🆘 Предупреждение: условие применимости теста не выполнено")
        print(f"   |ζ - 0.5| = {abs(pi - 0.5):.4f} >= {2/math.sqrt(n):.4f}")
        return 0.0
    
    # Вычисление V_N - числа знакоперемен (количество смен битов)
    v_n = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            v_n += 1
    
    # Вычисление P-value по формуле
    numerator = abs(v_n - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    
    if denominator == 0:
        return 0.0
    
    p_value = erfc(numerator / denominator)
    
    return p_value

def longest_run_test(sequence):
    """
    Тест на самую длинную последовательность единиц в блоке
    Формула из методички:
    Для N = 128 бит, M = 8
    v₁ = кол-во блоков с макс. длиной ≤ 1
    v₂ = кол-во блоков с макс. длиной = 2
    v₃ = кол-во блоков с макс. длиной = 3
    v₄ = кол-во блоков с макс. длиной ≥ 4
    
    χ² = Σ (v_i - 16π_i)² / (16π_i)
    π₀ = 0.2148, π₁ = 0.3672, π₂ = 0.2305, π₃ = 0.1875
    
    P_value = igamc(3/2, χ²/2)
    """
    # Проверяем, что последовательность содержит 128 бит
    if len(sequence) != 128:
        print(f"⛔ Ошибка: для теста нужно 128 бит, получено {len(sequence)}")
        return 0.0
    
    #Тестим
    test_seq = sequence[:128]
    m = 8  # длина блока
    num_blocks = 16  # 128 / 8 = 16 блоков
    
    # Теоретические вероятности из методички
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    
    # Подсчет максимальных длин серий единиц в каждом блоке
    v = [0, 0, 0, 0]  # v₀, v₁, v₂, v₃
    
    for i in range(num_blocks):
        block = test_seq[i*m:(i+1)*m]
        
        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        # Классификация по длине максимальной серии (строго по методичке)
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:  # max_run >= 4
            v[3] += 1
    
    print(f"📉 Распределение блоков: v₁={v[0]}, v₂={v[1]}, v₃={v[2]}, v₄={v[3]}")
    
    # Вычисление статистики хихихи-квадрат
    chi_square = 0
    for i in range(4):
        expected = num_blocks * pi[i]
        chi_square += ((v[i] - expected) ** 2) / expected
    
    print(f"   x² = {chi_square:.4f}")
    
    # Вычисление пи-валуе
    p_value = igamc(3/2, chi_square / 2)
    
    return p_value

def test_sequence(filename):
    """Тестирование последовательности из файла"""
    print(f"\n{'='*60}")
    print(f"ТЕСТИРОВАНИЕ ФАЙЛА: {filename}")
    print(f"{'='*60}")
    
    sequence = read_sequence(filename)
    if sequence is None:
        return
    
    n = len(sequence)
    zeros = sequence.count(0)
    ones = sequence.count(1)
    
    print(f"Длина последовательности: {n} бит (должно быть 128)")
    print(f"Количество нулей: {zeros} ({zeros/n*100:.1f}%)")
    print(f"Количество единиц: {ones} ({ones/n*100:.1f}%)")
    
    # Поиск максимальных серий
    max_zeros, max_ones = find_max_run(sequence)
    print(f"\nМАКСИМАЛЬНЫЕ СЕРИИ:")
    print(f"   Максимальная серия нулей: {max_zeros}")
    print(f"   Максимальная серия единиц: {max_ones}")
    
    print(f"\n{'-'*60}")
    print("📝ТЕСТЫ NIST:")
    print(f"{'-'*60}")
    
    print(f"\n🎰 1. ЧАСТОТНЫЙ ПОБИТОВЫЙ ТЕСТ")
    print(f"   Формула: P_value = erfc(|S_N|/√2)")
    p_freq = frequency_test(sequence)
    print(f"   P_value = {p_freq:.6f}")
    print(f"   Результат: {'СЛУЧАЙНАЯ' if p_freq >= 0.01 else 'НЕ СЛУЧАЙНАЯ'}")
    
    print(f"\n🔃 2. ТЕСТ НА ОДИНАКОВЫЕ ПОДРЯД ИДУЩИЕ БИТЫ")
    print(f"   Формула: P_value = erfc(|V_N - 2Nζ(1-ζ)| / (2√(2N) ζ(1-ζ)))")
    p_runs = runs_test(sequence)
    print(f" 👉 P_value = {p_runs:.6f}")
    print(f" 🌙 Результат: {'СЛУЧАЙНАЯ' if p_runs >= 0.01 else 'НЕ СЛУЧАЙНАЯ'}")
    
    print(f"\n3. ТЕСТ НА САМУЮ ДЛИННУЮ ПОСЛЕДОВАТЕЛЬНОСТЬ ЕДИНИЦ В БЛОКЕ")
    print(f"   Формула: P_value = igamc(3/2, x²/2)")
    p_long = longest_run_test(sequence)
    print(f"   P_value = {p_long:.6f}")
    print(f"   Результат: {'СЛУЧАЙНАЯ' if p_long >= 0.01 else 'НЕ СЛУЧАЙНАЯ'}")
    
    print(f"\n{'='*60}")
    print("📝 ВЫВОД:")
    if p_freq >= 0.01 and p_runs >= 0.01 and p_long >= 0.01:
        print("😍 Последовательность прошла все три теста NIST")
        print("😍 Может считаться случайной с уровнем значимости 0.01")
    else:
        print("😓 Последовательность НЕ прошла некоторые тесты")
        print("😖 Не может считаться случайной")
    print(f"{'='*60}")

def main():
    """Главная функция"""
    print("✋ ПРОГРАММА СТАТИСТИЧЕСКОГО АНАЛИЗА ПСЕВДОСЛУЧАЙНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
    print("✨ Три теста линейки NIST")
    print("🔃 Длина последовательности: 128 бит")
    print("🎯 Критерий: последовательность случайна, если P_value ≥ 0.01")
    
    if len(sys.argv) > 1:
        # Тестирование конкретного файла
        test_sequence(sys.argv[1])
    else:
        # Тестирование файлов по умолчанию
        files = ["D:\isb-2026\Lab2_20\sequence_cpp.txt", "D:\isb-2026\Lab2_20\sequence_java.txt"]
        
        for file in files:
            try:
                with open(file, 'r') as f:
                    test_sequence(file)
            except FileNotFoundError:
                print(f"\nФайл {file} не найден. Сначала запустите генераторы.")
                print("C++: ./generator.cpp")
                print("Java: java Generator")

if __name__ == "__main__":
    main()
    
'''Были реализованы три теста из линейки НИСТ:

Частотный побитовый тест — проверяет равномерность распределения нулей и единиц.

Тест на одинаковые подряд идущие биты — проверяет частоту смены битов.

Тест на самую длинную последовательность единиц в блоке — проверяет максимальные серии единиц в блоках по 8 бит.

Если останутся вопросы, ты можешь мне их задать!'''