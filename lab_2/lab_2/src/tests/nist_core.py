# lab_2/src/tests/nist_core.py
"""
Ядро тестов NIST для проверки случайности бинарных последовательностей
Реализация по методичке Лабораторной работы №2 (СГАУ, 2023)
"""

import math
from typing import List, Dict, Optional


class NISTTests:
    """Класс для выполнения трёх тестов NIST"""
    
    ALPHA = 0.01  # Порог значимости
    
    @staticmethod
    def monobit_test(sequence: str) -> float:
        """
        Частотный побитовый тест (Frequency Monobit Test)
        
        Проверяет соотношение единиц и нулей.
        Формула из методички (стр. 9-10):
        - S = Σ(2*ε_i - 1), где ε_i ∈ {0,1}
        - s_obs = |S| / √n
        - P = erfc(s_obs / √2)
        
        :param sequence: строка из '0' и '1'
        :return: p-value
        """
        n = len(sequence)
        if n == 0:
            return 0.0
        
        # Преобразуем: '1' → +1, '0' → -1
        transformed_sum = sum(1 if bit == '1' else -1 for bit in sequence)
        
        # Вычисляем статистику
        s_obs = abs(transformed_sum) / math.sqrt(n)
        
        # P-value через дополнительную функцию ошибок
        p_value = math.erfc(s_obs / math.sqrt(2))
        
        return p_value
    
    @staticmethod
    def runs_test(sequence: str) -> float:
        """
        Тест на одинаковые подряд идущие биты (Runs Test)
        
        Проверяет частоту переключений между 0 и 1.
        Формула из методички (стр. 10-11):
        - π = (количество единиц) / n
        - Проверка: |π - 0.5| < 2/√n, иначе P=0
        - V_n = количество переключений (0→1 или 1→0)
        - P = erfc(|V_n - 2nπ(1-π)| / (2√(2n)π(1-π)))
        
        :param sequence: строка из '0' и '1'
        :return: p-value
        """
        n = len(sequence)
        if n == 0:
            return 0.0
        
        # Доля единиц
        ones = sum(1 for bit in sequence if bit == '1')
        pi = ones / n
        
        # ✅ ПРОВЕРКА УСЛОВИЯ: если не выполнено — тест не проходит
        if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
            return 0.0
        
        # ✅ ПОДСЧЁТ ПЕРЕХОДОВ (runs): считаем смены 0↔1
        runs = 0
        for i in range(n - 1):
            if sequence[i] != sequence[i + 1]:
                runs += 1
        
        # Вычисляем статистику
        expected_runs = 2 * n * pi * (1 - pi)
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        
        if denominator == 0:
            return 0.0
        
        s_obs = abs(runs - expected_runs) / denominator
        
        # P-value
        p_value = math.erfc(s_obs / math.sqrt(2))
        
        return p_value
    
    @staticmethod
    def longest_run_ones_test(sequence: str, block_size: int = 8) -> float:
        """
        Тест на самую длинную последовательность единиц в блоке
        
        Разбивает последовательность на блоки и анализирует
        распределение максимальных серий единиц.
        Формула из методички (стр. 11-12):
        - Разбиваем на блоки длиной M=8 (для n=128)
        - В каждом блоке ищем max_run (самая длинная серия '1')
        - Категоризуем: v_0 (≤1), v_1 (=2), v_2 (=3), v_3 (≥4)
        - Вычисляем χ² = Σ((v_i - N·π_i)² / (N·π_i))
        - P = igamc(3/2, χ²/2)
        
        :param sequence: строка из '0' и '1' длиной 128
        :param block_size: размер блока (по умолчанию 8)
        :return: p-value
        """
        n = len(sequence)
        if n != 128:
            # Для других длин можно адаптировать, но по методичке — 128 бит
            pass
        
        num_blocks = n // block_size  # 16 блоков для 128 бит
        
        # ✅ КАТЕГОРИЗАЦИЯ: считаем в какие категории попадают блоки
        counts = [0, 0, 0, 0]  # v_0, v_1, v_2, v_3
        
        for i in range(num_blocks):
            block_start = i * block_size
            block_end = block_start + block_size
            block = sequence[block_start:block_end]
            
            # Поиск максимальной серии единиц в блоке
            max_run = 0
            current_run = 0
            
            for bit in block:
                if bit == '1':
                    current_run += 1
                    max_run = max(max_run, current_run)
                else:
                    current_run = 0
            
            # ✅ КЛАССИФИКАЦИЯ по методичке (стр. 11)
            if max_run <= 1:
                counts[0] += 1  # v_0
            elif max_run == 2:
                counts[1] += 1  # v_1
            elif max_run == 3:
                counts[2] += 1  # v_2
            else:  # max_run >= 4
                counts[3] += 1  # v_3
        
        # ✅ ТЕОРЕТИЧЕСКИЕ ВЕРОЯТНОСТИ (из методички, стр. 12)
        pi_values = [0.2148, 0.3672, 0.2305, 0.1875]
        
        # ✅ ВЫЧИСЛЕНИЕ ХИ-КВАДРАТ
        chi_squared = 0.0
        for i in range(4):
            expected = num_blocks * pi_values[i]
            observed = counts[i]
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        
        # ✅ P-VALUE через неполную гамма-функцию
        # Формула: P = igamc(3/2, χ²/2)
        # Используем внешнюю реализацию (scipy или аппроксимация)
        a = 3 / 2
        x = chi_squared / 2
        
        # Если scipy доступен — используем его
        try:
            from scipy.special import gammaincc
            p_value = gammaincc(a, x)
        except ImportError:
            # ✅ АППРОКСИМАЦИЯ неполной гамма-функции (если scipy нет)
            p_value = NISTTests._incomplete_gamma_approx(a, x)
        
        return p_value
    
    @staticmethod
    def _incomplete_gamma_approx(a: float, x: float) -> float:
        """
        Аппроксимация неполной гамма-функции igamc(a, x)
        Для случая a = 3/2 (как в тесте longest_run_ones)
        
        :param a: параметр формы (должен быть 1.5)
        :param x: значение (χ²/2)
        :return: приближённое значение P
        """
        if x < 0:
            return 1.0
        
        # Для a = 3/2: igamc(3/2, x) = erfc(√x) + (2/√π)·√x·e^(-x)
        # Но используем численное интегрирование для универсальности
        
        # Простая аппроксимация через ряд
        if x == 0:
            return 1.0
        
        # Метод продолженной дроби (упрощённый)
        result = 1.0
        term = 1.0
        
        for k in range(1, 50):
            term *= -x / (a + k)
            result += term
            if abs(term) < 1e-10:
                break
        
        # Нормализация
        import math
        gamma_a = math.gamma(a)
        normalized = result * math.exp(-x) * (x ** a) / gamma_a
        
        return max(0.0, min(1.0, 1.0 - normalized))
    
    @classmethod
    def is_random(cls, p_values: Dict[str, float]) -> bool:
        """
        Определяет, прошла ли последовательность все тесты
        
        :param p_values: словарь {название_теста: p_value}
        :return: True если все P-value >= ALPHA
        """
        return all(p >= cls.ALPHA for p in p_values.values())