import os
import hashlib
import tempfile
import unittest
from hash import calculating_hash, integrity_check, collision_demo
from load_and_save_hash import save_hash, load_hash


class TestHashApp(unittest.TestCase):
    def setUp(self) -> None:
        """
        Создает временные файлы и тестовые данные перед запуском каждого теста.
        """
        self.test_content = b"Hello, World!"
        self.expected_hash = hashlib.sha256(self.test_content).hexdigest()


        self.src_file = tempfile.NamedTemporaryFile(delete=False)
        self.src_file.write(self.test_content)
        self.src_file.close()

        self.hash_file = tempfile.NamedTemporaryFile(delete=False)
        self.hash_file.close()

    def tearDown(self) -> None:
        """
        Удаляет временные файлы после завершения каждого теста.
        """
        if os.path.exists(self.src_file.name):
            os.remove(self.src_file.name)
        if os.path.exists(self.hash_file.name):
            os.remove(self.hash_file.name)

    def test_calculating_hash(self) -> None:
        """
        Проверяет корректность расчета SHA-256 для созданного файла.
        """
        result_hash = calculating_hash(self.src_file.name)
        self.assertEqual(result_hash, self.expected_hash)

    def test_save_and_load_hash(self) -> None:
        """
        Проверяет, что хеш правильно сохраняется в файл и успешно считывается оттуда.
        """
        save_hash(self.src_file.name, self.expected_hash, self.hash_file.name)
        loaded_hash = load_hash(self.hash_file.name)
        self.assertEqual(loaded_hash, self.expected_hash)

    def test_integrity_check_success(self) -> None:
        """
        Проверяет, что проверка целостности возвращает True, если файл не изменен.
        """
        save_hash(self.src_file.name, self.expected_hash, self.hash_file.name)
        self.assertTrue(integrity_check(self.src_file.name, self.hash_file.name))

    def test_integrity_check_failure(self) -> None:
        """
        Проверяет, что проверка целостности возвращает False, если файл был изменен.
        """
        save_hash(self.src_file.name, self.expected_hash, self.hash_file.name)

        with open(self.src_file.name, "wb") as f:
            f.write(b"Modified content")

        self.assertFalse(integrity_check(self.src_file.name, self.hash_file.name))

    def test_collision_demo_structure(self) -> None:
        """
        Проверяет структуру возвращаемого словаря и базовую работу поиска коллизий.
        """
        result = collision_demo(attempts=10, prefix_len=1)
        
        self.assertIn("attempts", result)
        self.assertIn("first", result)
        self.assertIn("second", result)
        self.assertIsInstance(result["attempts"], int)


if __name__ == "__main__":
    unittest.main()