"""
Лабораторная работа №2
Статистический анализ псевдослучайных последовательностей
Реализация трёх тестов NIST SP 800-22
"""

import math
from scipy import special  # Для gammaincc в третьем тесте


def load_bits(filename: str) -> list[int]:
    """
    Загрузить битовую последовательность из текстового файла.
    
    Аргументы:
        filename: Путь к файлу с последовательностью (строка из 0 и 1)
    
    Возвращает:
        list[int]: Список битов [0, 1, 0, 1, ...]
    """
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().strip()
        return [int(ch) for ch in text if ch in '01']


def monobit_test(bits: list[int], alpha: float = 0.01) -> dict:
    """
    2.1 Частотный побитовый тест (Frequency Monobit Test).
    
    Проверяет, что количество единиц и нулей примерно одинаково.
    Формулы из методички:
        S = Σ(2·bit - 1), где bit ∈ {0,1} → {-1,+1}
        S_obs = |S| / √N
        P-value = erfc(S_obs / √2)
    
    Аргументы:
        bits: Список битов
        alpha: Уровень значимости (по умолчанию 0.01)
    
    Возвращает:
        dict: Результаты теста
    """
    N = len(bits)
    
    # Вычисление статистики S
    S = sum(2 * bit - 1 for bit in bits)
    S_obs = abs(S) / math.sqrt(N)
    
    # P-value через дополнительную функцию ошибок
    p_value = math.erfc(S_obs / math.sqrt(2))
    
    return {
        "name": "Частотный побитовый тест",
        "p_value": round(p_value, 6),
        "passed": p_value >= alpha,
        "details": f"S={S}, S_obs={S_obs:.4f}"
    }


def runs_test(bits: list[int], alpha: float = 0.01) -> dict:
    """
    2.2 Тест на одинаковые подряд идущие биты (Runs Test).
    
    Проверяет частоту переключений между 0 и 1.
    Формулы из методички:
        π = Σbits / N
        Предусловие: |2π - 1| < 2/√N
        V_n = 1 + количество переходов (0→1 или 1→0)
        P-value = erfc(|V_n - 2Nπ(1-π)| / (2√(2N)·π·(1-π)))
    
    Аргументы:
        bits: Список битов
        alpha: Уровень значимости
    
    Возвращает:
        dict: Результаты теста
    """
    N = len(bits)
    
    # Доля единиц
    pi = sum(bits) / N
    
    # Проверка предусловия
    if abs(2 * pi - 1) >= 2 / math.sqrt(N):
        return {
            "name": "Тест на одинаковые идущие подряд биты",
            "p_value": 0.0,
            "passed": False,
            "details": "Предусловие не выполнено"
        }
    
    # Подсчёт числа знакоперемен (серий)
    V_n = 1 + sum(1 for i in range(1, N) if bits[i] != bits[i-1])
    
    # Вычисление P-value
    numerator = abs(V_n - 2 * N * pi * (1 - pi)+1)
    denominator = 2 * math.sqrt(2 * N) * pi * (1 - pi)
    
    if denominator == 0:
        return {
            "name": "Тест на одинаковые идущие подряд биты",
            "p_value": 0.0,
            "passed": False,
            "details": "Ошибка вычисления"
        }
    
    p_value = math.erfc(numerator / denominator)
    
    return {
        "name": "Тест на одинаковые идущие подряд биты",
        "p_value": round(p_value, 6),
        "passed": p_value >= alpha,
        "details": f"V_n={V_n}, Expected={2*N*pi*(1-pi)+1:.2f}"
    }


def longest_run_test(bits: list[int], alpha: float = 0.01) -> dict:
    """
    2.3 Тест на самую длинную последовательность единиц в блоке.
    
    Для N=128 бит: M=8 (размер блока), 16 блоков, 4 категории.
    Формулы из методички:
        v₀: кол-во блоков с max_run ≤ 1
        v₁: кол-во блоков с max_run = 2
        v₂: кол-во блоков с max_run = 3
        v₃: кол-во блоков с max_run ≥ 4
        χ² = Σ(vⱼ - 16·πⱼ)² / (16·πⱼ)
        P-value = gammaincc(1.5, χ²/2)
    
    Аргументы:
        bits: Список битов
        alpha: Уровень значимости
    
    Возвращает:
        dict: Результаты теста
    """
    N = len(bits)
    M = 8  # Размер блока для 128 бит (из методички)
    num_blocks = N // M  # 16 блоков
    
    # Теоретические вероятности из методички
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    
    # Счётчики категорий
    v = [0, 0, 0, 0]
    
    # Обработка каждого блока
    for i in range(num_blocks):
        block = bits[i*M : (i+1)*M]
        
        # Поиск максимальной серии единиц в блоке
        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        # Финальная проверка (если блок заканчивается на 1)
        max_run = max(max_run, current_run)
        
        # Классификация по категориям
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:  # max_run >= 4
            v[3] += 1
    
    # Вычисление χ² (хи-квадрат)
    chi_sq = sum(
        (v[j] - num_blocks * pi[j])**2 / (num_blocks * pi[j])
        for j in range(4)
    )
    
    # P-value через неполную гамма-функцию
    # Параметр: (K-1)/2 = (4-1)/2 = 1.5
    p_value = special.gammaincc(1.5, chi_sq / 2)
    
    return {
        "name": "Тест на самую длинную серию единиц",
        "p_value": round(p_value, 6),
        "passed": p_value >= alpha,
        "details": f"χ²={chi_sq:.4f}, v={v}"
    }


def main():
    """Основная функция: запуск тестов для сгенерированных файлов."""
    
    files = ["cpp_seq.txt", "java_seq.txt"]
    alpha = 0.01
    
    
    for filename in files:
        print(f"\n📄 Файл: {filename}")
        
        try:
            bits = load_bits(filename)
            

            results = [
                monobit_test(bits, alpha),
                runs_test(bits, alpha),
                longest_run_test(bits, alpha)
            ]
            
            print("\nРЕЗУЛЬТАТЫ ТЕСТОВ:")
            all_passed = True
            
            for r in results:
                status = "ПРОЙДЕН" if r["passed"] else "НЕ ПРОЙДЕН"
                print(f"\n{r['name']}:")
                print(f"  Статус: {status}")
                print(f"  P-value: {r['p_value']}")
                
                if not r["passed"]:
                    all_passed = False
            
            if all_passed:
                print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
            else:
                print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
            
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден")
        except Exception as e:
            print(f"Ошибка: {e}")
    


if __name__ == "__main__":
    main()
