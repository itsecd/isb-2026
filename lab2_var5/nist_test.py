import math
import os
from collections import Counter
from scipy.special import gammaincc


class NISTTests:
    """Класс для проведения NIST тестов на бинарных последовательностях."""

    @staticmethod
    def read_sequence(filename):
        """
        Чтение бинарной последовательности из файла.

        Args:
            filename (str): Имя файла с последовательностью

        Returns:
            list: Список целых чисел (0 и 1) или None при ошибке
        """
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
            # Убираем возможные пробелы и переносы строк
            content = content.replace(' ', '').replace('\n', '')
            content = content.replace('\r', '')
            return [int(bit) for bit in content]
        except FileNotFoundError:
            return None
        except ValueError:
            return None

    @staticmethod
    def frequency_test(sequence):
        """
        Частотный побитовый тест (Frequency Test).

        Проверяет, близка ли доля единиц к 1/2.

        Args:
            sequence (list): Список битов

        Returns:
            dict: Результаты теста
        """
        n = len(sequence)
        if n == 0:
            return {"error": "Пустая последовательность"}

        # Подсчет единиц и нулей
        ones = sum(sequence)
        zeros = n - ones

        # Статистика теста S_obs
        s_obs = abs(ones - zeros) / math.sqrt(n)

        # p-value
        p_value = math.erfc(s_obs / math.sqrt(2))

        results = {
            'test_name': 'Частотный побитовый тест',
            'n': n,
            'ones': ones,
            'zeros': zeros,
            'ones_percent': (ones / n) * 100,
            'zeros_percent': (zeros / n) * 100,
            's_obs': s_obs,
            'p_value': p_value,
            'passed': p_value > 0.01  # уровень значимости 1%
        }

        return results

    @staticmethod
    def runs_test(sequence):
        """
        Тест на одинаковые подряд идущие биты (Runs Test).

        Проверяет, соответствует ли количество серий случайному
        распределению.

        Args:
            sequence (list): Список битов

        Returns:
            dict: Результаты теста
        """
        n = len(sequence)
        if n == 0:
            return {"error": "Пустая последовательность"}

        # Доля единиц
        ones = sum(sequence)
        pi = ones / n

        # Проверяем применимость теста
        threshold = 2 / math.sqrt(n)
        if abs(pi - 0.5) >= threshold:
            return {
                'test_name': 'Тест на серии',
                'error': (
                    f'Тест неприменим: доля единиц = {pi:.4f} '
                    f'(требуется |pi - 0.5| < {threshold:.4f})'
                ),
                'pi': pi,
                'threshold': threshold
            }

        # Подсчет серий
        v_n = 0
        for i in range(1, n):
            if sequence[i] != sequence[i-1]:
                v_n += 1
        runs = v_n + 1

        # Вычисление P-значения по формуле
        numerator = abs(v_n - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n * pi * (1 - pi))
        p_value = math.erfc(numerator / denominator)

        results = {
            'test_name': 'Тест на серии',
            'n': n,
            'ones': ones,
            'pi': pi,
            'runs': runs,
            'v_n': v_n,
            'p_value': p_value,
            'passed': p_value > 0.01
        }

        return results

    @staticmethod
    def longest_run_test(sequence):
        """
        Тест на самую длинную последовательность единиц в блоке (Longest Run Test).

        Проверяет распределение максимальных серий единиц по блокам.

        Args:
            sequence (list): Список битов

        Returns:
            dict: Результаты теста
        """
        n = len(sequence)
        if n < 128:
            return {"error": "Последовательность должна быть не менее 128 бит"}
        
        # Используем только первые 128 бит
        if n > 128:
            sequence = sequence[:128]
        
        # Разбиваем на блоки по 8 бит
        M = 8
        blocks = [sequence[i:i+M] for i in range(0, 128, M)]
        
        v = [0, 0, 0, 0]
        
        for block in blocks:
            # Поиск максимальной последовательности единиц в блоке
            max_run = 0
            current_run = 0
            for bit in block:
                if bit == 1:
                    current_run += 1
                    max_run = max(max_run, current_run)
                else:
                    current_run = 0
            
            # Распределение по категориям
            if max_run <= 1:
                v[0] += 1
            elif max_run == 2:
                v[1] += 1
            elif max_run == 3:
                v[2] += 1
            else:  # max_run >= 4
                v[3] += 1
        
        pi = [0.2148, 0.3672, 0.2305, 0.1875]
        
        chi_square = 0
        expected = [16 * p for p in pi]  
        for i in range(4):
            chi_square += ((v[i] - expected[i]) ** 2) / expected[i]
        
        # Вычисление P-значения через неполную гамма-функцию
        p_value = gammaincc(1.5, chi_square / 2)
        
        return {
            'test_name': 'Тест на самую длинную последовательность единиц',
            'blocks': 16,
            'block_size': 8,
            'observed': v,
            'expected': expected,
            'chi_square': chi_square,
            'p_value': p_value,
            'passed': p_value > 0.01
        }


def main():
    """Основная функция для тестирования всех последовательностей."""
    # Список файлов для тестирования
    TEST_FILES = [
        'java_sequence.txt',
        'cpp_sequence.txt',
        'python_sequence.txt'
    ]

    # Проверяем существование файлов
    existing_files = []
    for filename in TEST_FILES:
        if os.path.exists(filename):
            existing_files.append(filename)
        else:
            print(f"Файл {filename} не найден")

    if not existing_files:
        return

    # Создаем файл для сохранения результатов
    with open('nist_test_results.txt', 'w', encoding='utf-8') as result_file:
        result_file.write("Результаты NIST тестов\n")
        
        all_results = {}

        for filename in existing_files:
            # Читаем последовательность
            sequence = NISTTests.read_sequence(filename)

            if sequence is None:
                continue

            # Запускаем тесты
            freq_result = NISTTests.frequency_test(sequence)
            runs_result = NISTTests.runs_test(sequence)
            longest_result = NISTTests.longest_run_test(sequence) 

            # Сохраняем результаты
            results = {
                'frequency': freq_result,
                'runs': runs_result,
                'longest': longest_result 
            }
            all_results[filename] = results

            # Записываем в файл
            result_file.write("_" * 40 + "\n")
            result_file.write(f"\nФайл: {filename}\n")
            
            # Частотный тест
            result_file.write(f"\n{freq_result['test_name']}:\n")
            result_file.write(f"  Длина: {freq_result['n']}\n")
            result_file.write(f"  Единицы: {freq_result['ones']} "
                              f"({freq_result['ones_percent']:.2f}%)\n")
            result_file.write(f"  p-value: {freq_result['p_value']:.6f}\n")
            status = 'Пройден' if freq_result['passed'] else 'Не пройден'
            result_file.write(f"  Статус: {status}\n")

            # Тест на серии
            result_file.write(f"\n{runs_result['test_name']}:\n")
            if 'error' in runs_result:
                result_file.write(f"  Ошибка: {runs_result['error']}\n")
            else:
                result_file.write(f"  Серий: {runs_result['runs']}\n")
                result_file.write(f"  p-value: {runs_result['p_value']:.6f}\n")
                status = 'Пройден' if runs_result['passed'] else 'Не пройден'
                result_file.write(f"  Статус: {status}\n")
            
            # Тест на самую длинную последовательность
            result_file.write(f"\n{longest_result['test_name']}:\n")
            if 'error' in longest_result:
                result_file.write(f"  Ошибка: {longest_result['error']}\n")
            else:
                result_file.write(f"  Блоков: {longest_result['blocks']}\n")
                result_file.write(f"  Наблюдаемые частоты: {longest_result['observed']}\n")
                result_file.write(f"  χ² = {longest_result['chi_square']:.4f}\n")
                result_file.write(f"  p-value: {longest_result['p_value']:.6f}\n")
                status = 'Пройден' if longest_result['passed'] else 'Не пройден'
                result_file.write(f"  Статус: {status}\n")

        # Итоговое заключение
        result_file.write("_" * 40 + "\n")
        result_file.write("Заключение\n")
     
        for filename, results in all_results.items():
            freq_passed = results['frequency']['passed']
            runs_result = results['runs']
            runs_passed = False if 'error' in runs_result else runs_result.get('passed', False)
            longest_passed = results['longest'].get('passed', False) if 'error' not in results['longest'] else False

            result_file.write(f"\n{filename}:\n")
            result_file.write(f"  Частотный тест: {'Пройден' if freq_passed else 'Не пройден'}\n")
            
            if 'error' in runs_result:
                result_file.write(f"  Тест на серии: неприменим\n")
            else:
                result_file.write(f"  Тест на серии: {'Пройден' if runs_passed else 'Не пройден'}\n")
            
            if 'error' in results['longest']:
                result_file.write(f"  Тест на длинные серии: {results['longest']['error']}\n")
            else:
                result_file.write(f"  Тест на длинные серии: {'Пройден' if longest_passed else 'Не пройден'}\n")


if __name__ == "__main__":
    main()