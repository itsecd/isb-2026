import unittest
from hash_units import generate_salt, calculate_hash
from checks import check_login, check_secure_user_data, check_unsecure_user_data


class TestAuthSystem(unittest.TestCase):

    def test_generate_salt_properties(self):
        """Проверка генератора соли: длина и уникальность."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        
        self.assertEqual(len(salt1), 32)
        self.assertNotEqual(salt1, salt2)


    def test_calculate_hash_length(self):
        """Проверка длины хэша стандарта SHA-3-256 (всегда 64 hex-символа)."""
        p_hash = calculate_hash("password123")
        self.assertEqual(len(p_hash), 64)


    def test_calculate_hash_without_salt(self):
        """Проверка хэширования без соли (детерминированность)."""
        hash1 = calculate_hash("secret_pass")
        hash2 = calculate_hash("secret_pass")

        self.assertEqual(hash1, hash2)


    def test_calculate_hash_with_salt(self):
        """Проверка, что соль меняет итоговый хэш для одного пароля."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        
        hash1 = calculate_hash("secret_pass", salt1)
        hash2 = calculate_hash("secret_pass", salt2)
        
        self.assertNotEqual(hash1, hash2)


    def test_check_login_valid_cases(self):
        """Проверка корректных логинов (границы от 3 до 20 символов)."""
        self.assertTrue(check_login("alb"))      
        self.assertTrue(check_login("minialbina"))  
        self.assertTrue(check_login("abracadabraboompalaa"))    
        self.assertTrue(check_login("bD_2006"))


    def test_check_login_invalid_length(self):
        """Проверка логинов с некорректной длиной (менее 3 или более 20)."""
        self.assertFalse(check_login(""))     
        self.assertFalse(check_login("ok"))    
        self.assertFalse(check_login("abracadabraboompalaboompala"))


    def test_check_login_invalid_characters(self):
        """Проверка логинов, содержащих запрещенные спецсимволы или пробелы."""
        self.assertFalse(check_login("admin@"))   
        self.assertFalse(check_login("user name"))
        self.assertFalse(check_login("root!"))


    def test_secure_data_valid(self):
        """Идеальная структура из JSON файла должна возвращать True."""
        valid_user_info = {
            "hash": "a" * 64,
            "salt": "b" * 32 
        }
        self.assertTrue(check_secure_user_data(valid_user_info, "test_user"))


    def test_secure_data_missing_fields(self):
        """Проверка реакции на отсутствие обязательных полей в словаре (False)."""
        no_salt = {"hash": "a" * 64}
        no_hash = {"salt": "b" * 32}
        empty_dict = {}
        
        self.assertFalse(check_secure_user_data(no_salt, "test_user"))
        self.assertFalse(check_secure_user_data(no_hash, "test_user"))
        self.assertFalse(check_secure_user_data(empty_dict, "test_user"))


    def test_secure_data_invalid_types(self):
        """Проверка реакции, если структура сломана внешним вмешательством."""
        self.assertFalse(check_secure_user_data("not_a_dict", "test_user"))
        self.assertFalse(check_secure_user_data("", "test_user"))
        self.assertFalse(check_secure_user_data(["hash", "salt"], "test_user"))


    def test_secure_data_invalid_lengths(self):
        """Проверка реакции на урезанные или пустые значения полей (False)."""
        bad_hash_len = {"hash": "short", "salt": "b" * 32}
        bad_salt_len = {"hash": "a" * 64, "salt": "short"}
        empty_fields = {"hash": "", "salt": ""}
        
        self.assertFalse(check_secure_user_data(bad_hash_len, "test_user"))
        self.assertFalse(check_secure_user_data(bad_salt_len, "test_user"))
        self.assertFalse(check_secure_user_data(empty_fields, "test_user"))


    def test_unsecure_data_valid(self):
        """Правильный чистый хэш из файла должен возвращать True."""
        self.assertTrue(check_unsecure_user_data("c" * 64, "test_user"))


    def test_unsecure_data_invalid(self):
        """Проверка ломаных данных в unsec режиме (False)."""
        self.assertFalse(check_unsecure_user_data("short_hash", "test_user")) 
        self.assertFalse(check_unsecure_user_data("", "test_user"))          
        self.assertFalse(check_unsecure_user_data({"hash": "123"}, "test_user"))


if __name__ == "__main__":
    unittest.main()
