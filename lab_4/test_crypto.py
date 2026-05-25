import unittest

from no_crack import hash_password_no_salt, hash_comparison_no_salt
from hash_generation import hash_password
from salt_generation import generate_salt

class TestPasswordStorageSystem(unittest.TestCase):

    def setUp(self):
        # Подготовка тестовых данных
        self.password = "SuperSecret123"
        self.wrong_password = "WrongPassword"
        self.static_db = {
            "test_user": {
                "salt": "none",
                "hash": hash_password_no_salt(self.password)
            }
        }

    def test_no_salt_determinism(self):
        """Check: without salt same passwords give identical hashes"""
        hash1 = hash_password_no_salt(self.password)
        hash2 = hash_password_no_salt(self.password)
        self.assertEqual(hash1, hash2, "Hashes without salt should be the same!")

    def test_with_salt_uniqueness(self):
        """Check: with salt same passwords give different hashes"""
        salt1 = generate_salt()
        salt2 = generate_salt()
        
        hash1 = hash_password(self.password, salt1)
        hash2 = hash_password(self.password, salt2)
        
        self.assertNotEqual(salt1, salt2, "Salts must be unique")
        self.assertNotEqual(hash1, hash2, "Hashes with different salts must be different")

    def test_no_salt_comparison(self):
        """Athorisation test in saltless scheme"""
        self.assertTrue(hash_comparison_no_salt(self.static_db, "test_user", self.password))
        self.assertFalse(hash_comparison_no_salt(self.static_db, "test_user", self.wrong_password))
        self.assertFalse(hash_comparison_no_salt(self.static_db, "non_existent_user", self.password))

if __name__ == '__main__':
    unittest.main()