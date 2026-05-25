import unittest
from auth import hash_function, check_password, login_user, register_user
from auth_no_salt import hash_function_no_salt, check_password_no_salt, login_user_no_salt, register_user_no_salt


class TestAuthSystem(unittest.TestCase):

    def setUp(self):
        """
        
        """
        self.mock_data = {}
        self.test_user = "user"
        self.test_password = "SecretPassword123"

    

    def test_bcrypt_hash_generation(self):
        """Проверяем, что хэш bcrypt успешно генерируется и не пустой"""
        hashed = hash_function(self.test_password)
        self.assertIsNotNone(hashed)
        self.assertNotEqual(hashed, "")
        self.assertTrue(hashed.startswith("$2b$"))

    def test_bcrypt_check_password_correct(self):
        """Проверяем успешную валидацию правильного пароля"""
        hashed = hash_function(self.test_password)
        self.assertTrue(check_password(self.test_password, hashed))

    def test_bcrypt_check_password_incorrect(self):
        """Проверяем, что неверный пароль не пройдет проверку"""
        hashed = hash_function(self.test_password)
        self.assertFalse(check_password("WrongPassword", hashed))

    def test_bcrypt_registration_success(self):
        """Проверяем успешную регистрацию нового пользователя"""
        result = register_user(self.test_user, self.test_password, self.mock_data)
        self.assertTrue(result)
        self.assertIn(self.test_user, self.mock_data)
        self.assertNotEqual(self.mock_data[self.test_user], self.test_password)

    def test_bcrypt_registration_duplicate(self):
        """Проверяем, что нельзя зарегистрировать существующего пользователя"""
        register_user(self.test_user, self.test_password, self.mock_data)
        result = register_user(self.test_user, "another_pass", self.mock_data)
        self.assertFalse(result)

    def test_bcrypt_login(self):
        """Проверяем работу функции входа (успех и провал)"""
        register_user(self.test_user, self.test_password, self.mock_data)
        self.assertTrue(login_user(self.test_user, self.test_password, self.mock_data))
        self.assertFalse(login_user(self.test_user, "wrong_pass", self.mock_data))
        self.assertFalse(login_user("unknown_user", self.test_password, self.mock_data))



    def test_sha256_hash_generation(self):
        """Проверяем генерацию хэша SHA-256 (должен быть длиной 64 символа)"""
        hashed = hash_function_no_salt(self.test_password)
        self.assertEqual(len(hashed), 64)
        expected_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        self.assertEqual(hash_function_no_salt("password"), expected_hash)

    def test_sha256_check_password(self):
        """Проверяем валидацию пароля для SHA-256"""
        hashed = hash_function_no_salt(self.test_password)
        self.assertTrue(check_password_no_salt(self.test_password, hashed))
        self.assertFalse(check_password_no_salt("wrong", hashed))

    def test_sha256_registration_and_login(self):
        """Комплексный тест регистрации и входа для режима без соли"""
        reg_result = register_user_no_salt(self.test_user, self.test_password, self.mock_data)
        self.assertTrue(reg_result)
        self.assertFalse(register_user_no_salt(self.test_user, "new_pass", self.mock_data))
        self.assertTrue(login_user_no_salt(self.test_user, self.test_password, self.mock_data))
        self.assertFalse(login_user_no_salt(self.test_user, "invalid", self.mock_data))


if __name__ == "__main__":
    unittest.main()