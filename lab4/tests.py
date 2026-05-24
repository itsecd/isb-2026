import unittest
import os
import gc
import sqlite3
from backend import Auth

class TestAuthSystem(unittest.TestCase):
    def setUp(self):
        self.test_db = "test.db"
        self.auth = Auth(db_path=self.test_db)

    def tearDown(self):
        self.auth.close()
        del self.auth
        gc.collect()
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except PermissionError:
                pass

    def test_database_initialization(self):
        self.assertTrue(os.path.exists(self.test_db))
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        self.assertIn("username", columns)
        self.assertIn("password_hash", columns)
        self.assertIn("salt", columns)
        self.assertIn("is_safe", columns)

    def test_unsafe_registration_and_verification(self):
        self.auth.unsafe_registration("vulnerable_user", "vulnerable_password")
        userdata = self.auth.db.fetch_user("vulnerable_user")
        
        self.assertIsNotNone(userdata)
        stored_hash, salt, is_safe = userdata
        self.assertIsNone(salt)
        self.assertEqual(is_safe, 0)
        self.assertEqual(stored_hash, "vulnerable_password".encode('utf-8').hex())
        
        self.assertTrue(self.auth.verify_user("vulnerable_user", "vulnerable_password"))
        self.assertFalse(self.auth.verify_user("vulnerable_user", "wrong_password"))

    def test_safe_registration_and_verification(self):
        self.auth.safe_registration("secure_user", "secure_password")
        userdata = self.auth.db.fetch_user("secure_user")
        
        self.assertIsNotNone(userdata)
        stored_hash, salt, is_safe = userdata
        self.assertIsNotNone(salt)
        self.assertEqual(is_safe, 1)
        self.assertNotEqual(stored_hash, "secure_password")
        
        self.assertTrue(self.auth.verify_user("secure_user", "secure_password"))
        self.assertFalse(self.auth.verify_user("secure_user", "wrong_password"))

    def test_empty_fields_validation(self):
        with self.assertRaises(ValueError):
            self.auth.unsafe_registration("", "password")
        with self.assertRaises(ValueError):
            self.auth.unsafe_registration("user", "")
        with self.assertRaises(ValueError):
            self.auth.safe_registration("", "password")
        with self.assertRaises(ValueError):
            self.auth.safe_registration("user", "")

    def test_duplicate_username_error(self):
        self.auth.unsafe_registration("duplicate_user", "password1")
        with self.assertRaises(sqlite3.IntegrityError):
            self.auth.unsafe_registration("duplicate_user", "password2")

    def test_verify_non_existent_user(self):
        self.assertFalse(self.auth.verify_user("non_existent_user", "password"))

    def test_bruteforce_collision_success(self):
        self.auth.unsafe_registration("victim", "123")
        userdata = self.auth.db.fetch_user("victim")
        captured_hash = userdata[0]
        
        found_password = self.auth.bruteforce(captured_hash)
        self.assertEqual(found_password, "123")

    def test_bruteforce_collision_failure(self):
        self.auth.unsafe_registration("victim", "vbieqi121uqiov1452uie562auio")
        userdata = self.auth.db.fetch_user("victim")
        captured_hash = userdata[0]
        
        found_password = self.auth.bruteforce(captured_hash)
        self.assertIsNone(found_password)

if __name__ == "__main__":
    output = "Report.txt"
    with open(output, "w", encoding="utf-8") as f:
        f.write("===Tests Report===\n\n")
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner, exit=False)
    print(f"[SUCCESS] Tests execution completed. Report saved to '{output}'")