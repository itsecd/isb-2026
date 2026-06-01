import unittest
import os
import sqlite3
from backend import Auth

class TestAuthSystem(unittest.TestCase):
    """
    Набор модульных тестов для проверки корректности работы системы аутентификации.
    
    Тестирует:
        - Регистрацию (безопасную и небезопасную)
        - Верификацию пользователей
        - Обработку некорректных входных данных
        - Различия между безопасным и небезопасным хешированием
        - Структуру базы данных
        - Демонстрацию брутфорс-атаки
    """
    
    def setUp(self):
        """
        Подготовка тестового окружения перед каждым тестом.
        
        Создаёт временную базу данных "test.db" и экземпляр Auth для тестирования.
        Запускается автоматически перед каждым тестовым методом.
        """
        self.db_path = "test.db"
        self.auth = Auth(db_path=self.db_path)

    def tearDown(self):
        """
        Очистка после выполнения каждого теста.
        
        Закрывает соединение с БД и удаляет временный файл базы данных.
        Запускается автоматически после каждого тестового метода.
        """
        self.auth.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_unsafe_registration(self):
        """
        Тест регистрации с небезопасным хешированием (SHA-256).
        
        Проверяет, что пользователь может зарегистрироваться с SHA-256
        и успешно войти с правильным паролем.
        """
        self.auth.unsafe_registration("user1", "pass1")
        result = self.auth.verify_user("user1", "pass1")
        self.assertTrue(result)

    def test_safe_registration(self):
        """
        Тест регистрации с безопасным хешированием (bcrypt + соль).
        
        Проверяет, что пользователь может зарегистрироваться с bcrypt
        и успешно войти с правильным паролем.
        """
        self.auth.safe_registration("user2", "pass2")
        result = self.auth.verify_user("user2", "pass2")
        self.assertTrue(result)

    def test_wrong_password(self):
        """
        Тест проверки пароля: неверный пароль должен отклоняться.
        
        Регистрирует пользователя с паролем "pass3", затем пытается войти
        с неверным паролем "wrong". Ожидается False.
        """
        self.auth.unsafe_registration("user3", "pass3")
        self.assertFalse(self.auth.verify_user("user3", "wrong"))

    def test_nonexistent_user(self):
        """
        Тест проверки несуществующего пользователя.
        
        Пытается выполнить вход для пользователя "ghost", которого нет в БД.
        Ожидается False.
        """
        self.assertFalse(self.auth.verify_user("ghost", "123"))

    def test_empty_fields(self):
        """
        Тест обработки пустых полей при регистрации.
        
        Проверяет, что регистрация с пустым именем пользователя или паролем
        вызывает исключение ValueError.
        """
        with self.assertRaises(ValueError):
            self.auth.unsafe_registration("", "pass")

        with self.assertRaises(ValueError):
            self.auth.safe_registration("user", "")

    def test_hash_difference_safe_vs_unsafe(self):
        """
        Тест различия между безопасным и небезопасным хешированием.
        
        Регистрирует двух пользователей с одинаковым паролем "samepass",
        но разными методами (unsafe и safe). Проверяет, что хеши различаются.
        
        Причина: bcrypt использует соль, SHA-256 - нет.
        """
        self.auth.unsafe_registration("a", "samepass")
        self.auth.safe_registration("b", "samepass")

        u1 = self.auth.db.fetch_user("a")
        u2 = self.auth.db.fetch_user("b")

        self.assertNotEqual(u1[0], u2[0])  # разные хеши

    def test_database_structure(self):
        """
        Тест структуры таблицы базы данных.
        
        Проверяет наличие всех необходимых колонок в таблице users:
            - username (имя пользователя)
            - password_hash (хеш пароля)
            - salt (соль)
            - is_safe (флаг безопасного хеширования)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("username", columns)
        self.assertIn("password_hash", columns)
        self.assertIn("salt", columns)
        self.assertIn("is_safe", columns)

    def test_bruteforce_success(self):
        """
        Тест успешного брутфорса.
        
        Регистрирует пользователя с простым паролем "123" (число).
        Запускает брутфорс по хешу и проверяет, что пароль найден.
        
        Ожидается: bruteforce() возвращает "123".
        """
        self.auth.unsafe_registration("victim", "123")
        row = self.auth.db.fetch_user("victim")

        found = self.auth.bruteforce(row[0])

        self.assertEqual(found, "123")

    def test_bruteforce_failure(self):
        """
        Тест неудачного брутфорса.
        
        Регистрирует пользователя со сложным паролем "complex_password_999",
        который не входит в диапазон перебора (0-4999).
        
        Ожидается: bruteforce() возвращает None (пароль не найден).
        """
        self.auth.unsafe_registration("victim2", "complex_password_999")
        row = self.auth.db.fetch_user("victim2")

        found = self.auth.bruteforce(row[0])

        self.assertIsNone(found)

if __name__ == "__main__":
    unittest.main(verbosity=2)