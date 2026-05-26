import unittest
import os
from hasher import calculate_file_hash, save_hash_to_file, verify_file_integrity


class TestHasherModule(unittest.TestCase):

    def setUp(self):
        """Создаем временные файлы для тестов."""
        self.test_file = "temp_test_file.txt"
        self.hash_file = "temp_test_hash.sha256"

        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Тестовые данные для лабораторной работы по ИБ.")

    def tearDown(self):
        """Удаляем временные файлы."""
        for path in [self.test_file, self.hash_file]:
            if os.path.exists(path):
                os.remove(path)

    def test_calculate_hash_success(self):
        """Тест успешного подсчета хеша."""
        h1 = calculate_file_hash(self.test_file)
        self.assertEqual(len(h1), 64)

    def test_file_not_found_exception(self):
        """Проверка реакции на отсутствие файла."""
        with self.assertRaises(FileNotFoundError):
            calculate_file_hash("non_existent_file.xyz")

    def test_integrity_success(self):
        """Проверка работы контроля целостности при неизменном файле."""
        h1 = calculate_file_hash(self.test_file)
        save_hash_to_file(h1, self.hash_file)

        is_valid, cur, exp = verify_file_integrity(
            self.test_file, self.hash_file)
        self.assertTrue(is_valid)
        self.assertEqual(cur, exp)

    def test_integrity_fail_on_modification(self):
        """Проверка детекции изменений в файле."""
        h1 = calculate_file_hash(self.test_file)
        save_hash_to_file(h1, self.hash_file)

        with open(self.test_file, "a", encoding="utf-8") as f:
            f.write("Изменение.")

        is_valid, cur, exp = verify_file_integrity(
            self.test_file, self.hash_file)
        self.assertFalse(is_valid)
        self.assertNotEqual(cur, exp)


if __name__ == "__main__":
    unittest.main()
