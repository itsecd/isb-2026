import unittest
import hashlib
from modules.hashing import (
    generate_salt,
    hash_password_sha256,
    hash_password_sha256_no_salt,
    hash_password_bcrypt,
    verify_password_sha256,
    verify_password_bcrypt,
    find_collision_simple
)


class TestGenerateSalt(unittest.TestCase):
    """Тесты для функции generate_salt."""

    def test_default_length(self):
        """Проверка что соль по умолчанию 16 байт."""
        salt = generate_salt()
        self.assertEqual(len(salt), 16)

    def test_custom_length(self):
        """Проверка генерации соли заданной длины."""
        salt = generate_salt(32)
        self.assertEqual(len(salt), 32)

    def test_randomness(self):
        """Проверка что две соли не совпадают."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        self.assertNotEqual(salt1, salt2)


class TestSHA256Hashing(unittest.TestCase):
    """Тесты для хеширования SHA-256."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.password = "test_password_123"
        self.salt = generate_salt()

    def test_hash_with_salt_returns_string(self):
        """Проверка что хеш возвращается строкой."""
        result = hash_password_sha256(self.password, self.salt)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_hash_without_salt_returns_string(self):
        """Проверка что хеш без соли тоже строка."""
        result = hash_password_sha256_no_salt(self.password)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_same_password_same_hash(self):
        """Одинаковые пароли с той же солью дают одинаковый хеш."""
        hash1 = hash_password_sha256(self.password, self.salt)
        hash2 = hash_password_sha256(self.password, self.salt)
        self.assertEqual(hash1, hash2)

    def test_different_salt_different_hash(self):
        """Разная соль даёт разный хеш для одного пароля."""
        salt2 = generate_salt()
        hash1 = hash_password_sha256(self.password, self.salt)
        hash2 = hash_password_sha256(self.password, salt2)
        self.assertNotEqual(hash1, hash2)

    def test_different_password_different_hash(self):
        """Разные пароли с той же солью дают разный хеш."""
        hash1 = hash_password_sha256(self.password, self.salt)
        hash2 = hash_password_sha256("different_password", self.salt)
        self.assertNotEqual(hash1, hash2)

    def test_verify_correct_password(self):
        """Проверка правильного пароля возвращает True."""
        hash_val = hash_password_sha256(self.password, self.salt)
        self.assertTrue(
            verify_password_sha256(self.password, self.salt, hash_val)
        )

    def test_verify_incorrect_password(self):
        """Проверка неправильного пароля возвращает False."""
        hash_val = hash_password_sha256(self.password, self.salt)
        self.assertFalse(
            verify_password_sha256("wrong_password", self.salt, hash_val)
        )


class TestBcryptHashing(unittest.TestCase):
    """Тесты для хеширования bcrypt."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.password = "test_password_123"
        self.salt = generate_salt()

    def test_hash_returns_string(self):
        """Проверка что bcrypt возвращает строку."""
        result = hash_password_bcrypt(self.password, self.salt)
        self.assertIsInstance(result, str)

    def test_same_password_different_hash(self):
        """Один и тот же пароль даёт разный хеш (из-за встроенной соли)."""
        hash1 = hash_password_bcrypt(self.password, self.salt)
        hash2 = hash_password_bcrypt(self.password, self.salt)
        self.assertNotEqual(hash1, hash2)

    def test_verify_correct_password(self):
        """Проверка правильного пароля."""
        hash_val = hash_password_bcrypt(self.password, self.salt)
        self.assertTrue(
            verify_password_bcrypt(self.password, hash_val)
        )

    def test_verify_incorrect_password(self):
        """Проверка неправильного пароля."""
        hash_val = hash_password_bcrypt(self.password, self.salt)
        self.assertFalse(
            verify_password_bcrypt("wrong_password", hash_val)
        )


class TestAvalancheEffect(unittest.TestCase):
    """Тесты для проверки лавинного эффекта."""

    def test_avalanche_sha256(self):
        """Проверка что изменение одного символа меняет хеш."""
        msg1 = "hello_world"
        msg2 = "hello_worle"

        hash1 = hashlib.sha256(msg1.encode()).hexdigest()
        hash2 = hashlib.sha256(msg2.encode()).hexdigest()

        self.assertNotEqual(hash1, hash2)

        bin1 = bin(int(hash1, 16))[2:].zfill(256)
        bin2 = bin(int(hash2, 16))[2:].zfill(256)

        diff_bits = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
        diff_percent = (diff_bits / 256) * 100

        self.assertGreater(diff_percent, 30)
        self.assertLess(diff_percent, 70)


class TestCollisionSearch(unittest.TestCase):
    """Тесты для поиска коллизии."""

    def test_find_collision_2_bytes(self):
        """Проверка что коллизия находится для 2 байт."""
        result = find_collision_simple(2, show_progress=False)
        self.assertIsNotNone(result["message1"])
        self.assertIsNotNone(result["message2"])
        self.assertEqual(
            result["hash_prefix"],
            hashlib.sha256(
                result["message1"].encode()
            ).hexdigest()[:4]
        )

    def test_find_collision_returns_dict(self):
        """Проверка структуры результата."""
        result = find_collision_simple(2, show_progress=False)
        self.assertIsInstance(result, dict)
        self.assertIn("message1", result)
        self.assertIn("message2", result)
        self.assertIn("hash_prefix", result)
        self.assertIn("attempts", result)
        self.assertIn("time_seconds", result)


if __name__ == '__main__':
    unittest.main()