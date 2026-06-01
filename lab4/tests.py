"""Юнит-тесты для системы аутентификации."""

import unittest
import os
from hash_utils import generate_salt, calculate_hash
from db_utils import write_json, safe_load
from auth import register_user, authenticate_user


class TestHashUtils(unittest.TestCase):
    """Тесты для модуля hash_utils."""

    def test_generate_salt_length(self):
        """Проверка длины соли."""
        salt = generate_salt()
        self.assertEqual(len(salt), 32)

    def test_generate_salt_unique(self):
        """Проверка уникальности соли."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        self.assertNotEqual(salt1, salt2)

    def test_generate_salt_invalid_length(self):
        """Проверка исключения при некорректной длине."""
        with self.assertRaises(ValueError):
            generate_salt(0)

    def test_calculate_hash_without_salt(self):
        """Проверка хеширования без соли."""
        hash1 = calculate_hash("password")
        hash2 = calculate_hash("password")
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

    def test_calculate_hash_with_salt(self):
        """Проверка хеширования с солью."""
        salt = generate_salt()
        hash1 = calculate_hash("password", salt)
        hash2 = calculate_hash("password", salt)
        self.assertEqual(hash1, hash2)

    def test_calculate_hash_different_salts(self):
        """Проверка, что разные соли дают разные хеши."""
        hash1 = calculate_hash("password", generate_salt())
        hash2 = calculate_hash("password", generate_salt())
        self.assertNotEqual(hash1, hash2)


class TestDbUtils(unittest.TestCase):
    """Тесты для модуля db_utils."""

    def setUp(self):
        """Создаёт временный файл перед тестами."""
        self.test_path = "test_db.json"

    def tearDown(self):
        """Удаляет временный файл после тестов."""
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_write_and_read_json(self):
        """Проверка записи и чтения JSON."""
        data = {"user": "hash"}
        write_json(self.test_path, data)
        loaded = safe_load(self.test_path)
        self.assertEqual(loaded, data)

    def test_safe_load_not_found(self):
        """Проверка safe_load при отсутствии файла."""
        result = safe_load("nonexistent.json")
        self.assertEqual(result, {})

    def test_safe_load_corrupted(self):
        """Проверка safe_load при повреждённом файле."""
        with open(self.test_path, "w", encoding="utf-8") as f:
            f.write("not a json")
        result = safe_load(self.test_path)
        self.assertIsNone(result)


class TestAuth(unittest.TestCase):
    """Тесты для модуля аутентификации."""

    def setUp(self):
        """Подготавливает временную базу данных."""
        self.db_path = "test_auth.json"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        """Удаляет временную базу данных."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_register_user_secure(self):
        """Проверка регистрации в безопасном режиме."""
        result = register_user("alice", "secret", self.db_path, use_salt=True)
        self.assertIn("успешно", result)

    def test_register_user_unsecure(self):
        """Проверка регистрации в небезопасном режиме."""
        result = register_user("bob", "pass", self.db_path, use_salt=False)
        self.assertIn("успешно", result)

    def test_register_duplicate(self):
        """Проверка регистрации существующего пользователя."""
        register_user("alice", "secret", self.db_path, use_salt=True)
        result = register_user("alice", "secret2", self.db_path, use_salt=True)
        self.assertIn("уже существует", result)

    def test_authenticate_success_secure(self):
        """Проверка успешной авторизации в безопасном режиме."""
        register_user("alice", "secret", self.db_path, use_salt=True)
        result = authenticate_user("alice", "secret", self.db_path, use_salt=True)
        self.assertIn("Добро пожаловать", result)

    def test_authenticate_success_unsecure(self):
        """Проверка успешной авторизации в небезопасном режиме."""
        register_user("bob", "pass", self.db_path, use_salt=False)
        result = authenticate_user("bob", "pass", self.db_path, use_salt=False)
        self.assertIn("Добро пожаловать", result)

    def test_authenticate_wrong_password(self):
        """Проверка авторизации с неверным паролем."""
        register_user("alice", "secret", self.db_path, use_salt=True)
        result = authenticate_user("alice", "wrong", self.db_path, use_salt=True)
        self.assertIn("Неверный пароль", result)

    def test_authenticate_nonexistent_user(self):
        """Проверка авторизации несуществующего пользователя."""
        register_user("alice", "secret", self.db_path, use_salt=True)
        result = authenticate_user("ghost", "pass", self.db_path, use_salt=True)
        self.assertIn("не найден", result)

    def test_register_empty_login(self):
        """Проверка регистрации с пустым логином."""
        with self.assertRaises(ValueError):
            register_user("", "pass", self.db_path, use_salt=True)

    def test_register_empty_password(self):
        """Проверка регистрации с пустым паролем."""
        with self.assertRaises(ValueError):
            register_user("alice", "", self.db_path, use_salt=True)


if __name__ == "__main__":
    unittest.main()