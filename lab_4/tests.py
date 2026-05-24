import unittest

from analysis_utils import count_bit_diff, diff_percent
from hash_utils import compute_hash
from mutation_utils import change_one_bit, change_one_char, change_register, apply_mutation


class TestHashUtils(unittest.TestCase):
    def test_hash_output_type(self):
        """Хеш-функция должна возвращать текстовую строку"""
        result = compute_hash("word", "sha256")
        self.assertIsInstance(result, str)

    def test_different_inputs_give_different_hashes(self):
        """Разный текст должен приводить к разным хешам"""
        hash1 = compute_hash("apple", "sha256")
        hash2 = compute_hash("apples", "sha256")
        self.assertNotEqual(hash1, hash2)

    def test_hash_empty_string(self):
        """Хеширование пустой строки должно успешно возвращать валидный хеш"""
        result = compute_hash("", "sha256")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_hash_unknown_algorithm(self):
        """Запрос несуществующего алгоритма должен вызывать ошибку ValueError"""
        with self.assertRaises(ValueError):
            compute_hash("word", "unknown_algo_123")


class TestMutationUtils(unittest.TestCase):
    def test_char_mutation_changes_text(self):
        """Изменение символа должно гарантированно изменить байты"""
        original = "char"
        mutated = change_one_char(original)
        self.assertIsInstance(mutated, bytes)
        self.assertNotEqual(original.encode("utf-8"), mutated)

    def test_bit_mutation_changes_text(self):
        """Изменение бита должно гарантированно изменить байты"""
        original = "bit"
        mutated = change_one_bit(original)
        self.assertIsInstance(mutated, bytes)
        self.assertNotEqual(original.encode("utf-8"), mutated)

    def test_register_mutation_changes_text(self):
        """Изменение регистра должно изменить исходную строку"""
        original = "register"
        mutated = change_register(original)
        self.assertIsInstance(mutated, bytes)
        self.assertNotEqual(original.encode("utf-8"), mutated)

    def test_apply_char_mutation(self):
        """Режим 'char' должен возвращать изменённые байты и корректное название операции"""
        original = "word"
        mutated, op = apply_mutation(original, "char")

        self.assertIsInstance(mutated, bytes)
        self.assertEqual(op, "Символ")
        self.assertNotEqual(original.encode("utf-8"), mutated)

    def test_register_mutation_no_letters(self):
        """Строка без букв при изменении регистра возвращается в виде байт без изменений"""
        original = "12345!!!"
        mutated = change_register(original)
        self.assertEqual(original.encode("utf-8"), mutated)

    def test_mutation_empty_string_error(self):
        """Попытка изменения символа в пустой строке должна вызывать ошибку ValueError"""
        with self.assertRaises(ValueError):
            change_one_char("")

    def test_apply_invalid_mode(self):
        """Неизвестный режим должен вызывать ValueError"""
        with self.assertRaises(ValueError):
            apply_mutation("hello", "unknown")


class TestAnalysisUtils(unittest.TestCase):
    def test_bit_diff_for_different_hashes(self):
        """Разница в битах между хешами, отличающимися на один символ"""
        hash_str1 = "a1b2c3d4"
        hash_str2 = "a1b2c3d5"
        result = count_bit_diff(hash_str1, hash_str2)
        self.assertEqual(result, 1)

    def test_percent_calculation_half(self):
        """Если изменилась половина бит, должно быть ровно 50%"""
        result = diff_percent(128, 256)
        self.assertEqual(result, 50.0)

    def test_bit_diff_for_identical_hashes(self):
        """Разница в битах между одинаковыми хешами должна быть равна 0"""
        hash_str = "a1b2c3d4"
        result = count_bit_diff(hash_str, hash_str)
        self.assertEqual(result, 0)

    def test_percent_calculation_zero(self):
        """Если ничего не изменилось, должно быть 0%"""
        result = diff_percent(0, 256)
        self.assertEqual(result, 0.0)

    def test_percent_calculation_max(self):
        """Если изменились абсолютно все биты, должно быть 100%"""
        result = diff_percent(256, 256)
        self.assertEqual(result, 100.0)

    def test_bit_diff_different_sizes(self):
        """Сравнение хешей разной длины должно вызывать ошибку ValueError"""
        with self.assertRaises(ValueError):
            count_bit_diff("a1b2", "a1b2c3")

    def test_percent_division_by_zero(self):
        """Передача total_bits=0 должна вызывать ошибку ValueError"""
        with self.assertRaises(ValueError):
            diff_percent(10, 0)

    def test_percent_diff_greater_than_total(self):
        """Если измененных бит больше, чем всего бит, должна вызываться ошибка ValueError"""
        with self.assertRaises(ValueError):
            diff_percent(300, 256)
