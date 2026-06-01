import unittest
import os
import hashlib
import bcrypt

import hasher
from UserManager import UserManager, UserManagerError
from UserStorage import UserStorage

class TestCryptoAndAuth(unittest.TestCase):

    def test_hash_simple_sha256(self):
        """
        Проверка базового хэширования SHA-256
        """
        password = "my_secret_password"
        
    
        result = hasher.hash_simple(password)
        
        self.assertEqual(result["algo"], "sha256")
        
        expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.assertEqual(result["hash"], expected_hash)

    def test_hash_salted_generates_valid_hex_and_hash(self):
        """
        Проверка генерации соли и хэширования с солью
        """
        password = "qwerty_salt_test"
        
        result = hasher.hash_salted(password)
        
        self.assertEqual(result["algo"], "sha256_salted")
        self.assertIn("salt", result)
        self.assertIn("hash", result)
       
        try:
            salt_bytes = bytes.fromhex(result["salt"])
        except ValueError:
            self.fail("Соль не является валидной HEX-строкой!")
            
        self.assertEqual(len(salt_bytes), 16) 

    def test_verify_password_correct(self):
        """
        Проверка успешной валидации правильных паролей для всех алгоритмов
        """
        password = "secure_pass_123"
        
        record_simple = hasher.hash_simple(password)
        record_salted = hasher.hash_salted(password)
        record_bcrypt = hasher.hash_bcrypt(password)
        
        
        self.assertTrue(hasher.verify_password(password, record_simple))
        self.assertTrue(hasher.verify_password(password, record_salted))
        self.assertTrue(hasher.verify_password(password, record_bcrypt))

    def test_verify_password_incorrect(self):
        """
        Проверка, что неверный пароль не пройдет проверку
        """
        password = "correct_password"
        wrong_password = "wrong_password"
        
        record_salted = hasher.hash_salted(password)
        
        
        self.assertFalse(hasher.verify_password(wrong_password, record_salted))

    

    def test_register_empty_login_or_password_raises_error(self):
        """
        Менеджер должен выбрасывать UserManagerError при пустых полях
        """
       
        storage = UserStorage(path="test_users.json")
        manager = UserManager(storage=storage)
        
        
        with self.assertRaises(UserManagerError):
            manager.register("", "password123")
            
       
        with self.assertRaises(UserManagerError):
            manager.register("user1", "")
            
       
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")

    def test_authenticate_non_existent_user(self):
        """
        Попытка входа несуществующим пользователем должна вызывать ошибку
        """
        storage = UserStorage(path="test_users.json")
        manager = UserManager(storage=storage)
        
        with self.assertRaises(UserManagerError):
            manager.authenticate("ghost_user", "some_password")
            
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")


if __name__ == "__main__":
    unittest.main()