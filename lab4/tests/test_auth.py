import unittest
import os
import tempfile
import json
from modules.auth import register_user, authenticate_user, list_users


class TestAuth(unittest.TestCase):
    """Тесты для функций аутентификации."""

    def setUp(self):
        """Создаёт временный файл для тестов."""
        self.temp_file = os.path.join(tempfile.gettempdir(),
                                     "test_users.json")
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def tearDown(self):
        """Удаляет временный файл после тестов."""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_register_new_user_sha256(self):
        """Регистрация нового пользователя с SHA-256."""
        result = register_user("testuser", "password123",
                              self.temp_file, "sha256")
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["user_data"])
        self.assertEqual(result["user_data"]["algorithm"], "sha256")
        self.assertIn("salt", result["user_data"])
        self.assertIn("hash", result["user_data"])

    def test_register_new_user_bcrypt(self):
        """Регистрация нового пользователя с bcrypt."""
        result = register_user("testuser2", "password456",
                              self.temp_file, "bcrypt")
        self.assertTrue(result["success"])
        self.assertEqual(result["user_data"]["algorithm"], "bcrypt")

    def test_register_duplicate_user(self):
        """Регистрация уже существующего пользователя."""
        register_user("duplicate", "pass1", self.temp_file)
        result = register_user("duplicate", "pass2", self.temp_file)
        self.assertFalse(result["success"])

    def test_register_empty_password_raises(self):
        """Регистрация с пустым паролем вызывает ошибку."""
        with self.assertRaises(ValueError):
            register_user("user", "", self.temp_file)

    def test_authenticate_valid_sha256(self):
        """Вход с правильным паролем SHA-256."""
        register_user("auth_test", "correct_pass",
                     self.temp_file, "sha256")
        result = authenticate_user("auth_test", "correct_pass",
                                  self.temp_file)
        self.assertTrue(result["success"])

    def test_authenticate_invalid_password(self):
        """Вход с неправильным паролем."""
        register_user("auth_test2", "correct_pass",
                     self.temp_file, "sha256")
        result = authenticate_user("auth_test2", "wrong_pass",
                                  self.temp_file)
        self.assertFalse(result["success"])

    def test_authenticate_nonexistent_user(self):
        """Вход несуществующего пользователя."""
        result = authenticate_user("ghost", "pass",
                                  self.temp_file)
        self.assertFalse(result["success"])

    def test_authenticate_valid_bcrypt(self):
        """Вход с правильным паролем bcrypt."""
        register_user("bcrypt_user", "bcrypt_pass",
                     self.temp_file, "bcrypt")
        result = authenticate_user("bcrypt_user", "bcrypt_pass",
                                  self.temp_file)
        self.assertTrue(result["success"])

    def test_list_users(self):
        """Получение списка пользователей."""
        register_user("user1", "pass1", self.temp_file)
        register_user("user2", "pass2", self.temp_file)

        users = list_users(self.temp_file)
        self.assertEqual(len(users), 2)
        usernames = [u["username"] for u in users]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)

    def test_user_data_persists(self):
        """Проверка что данные сохраняются между вызовами."""
        register_user("persist_user", "persist_pass",
                     self.temp_file, "sha256")

        with open(self.temp_file, 'r') as f:
            data = json.load(f)

        self.assertIn("persist_user", data)
        self.assertIn("hash", data["persist_user"])
        self.assertIn("salt", data["persist_user"])


if __name__ == '__main__':
    unittest.main()