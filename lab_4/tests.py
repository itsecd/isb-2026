import unittest
from hash_utils import generate_random_string, compute_full_hash, truncate_hash, get_hash
from attack import find_collision, get_expected_attempts


class TestHashUtils(unittest.TestCase):
    """Тесты для утилит хеширования."""

    def test_generate_random_string(self):
        s = generate_random_string(10)
        self.assertEqual(len(s), 10)

        s = generate_random_string()
        self.assertGreaterEqual(len(s), 10)
        self.assertLessEqual(len(s), 100)

        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self.assertTrue(all(c in valid_chars for c in s))

    def test_compute_full_hash(self):
        h1 = compute_full_hash("test")
        h2 = compute_full_hash("test")
        self.assertEqual(h1, h2)

        h1 = compute_full_hash("test1")
        h2 = compute_full_hash("test2")
        self.assertNotEqual(h1, h2)

        self.assertEqual(len(compute_full_hash("test")), 64)

    def test_truncate_hash(self):
        full_hash = "a1b2c3d4e5f67890"
        self.assertEqual(truncate_hash(full_hash, 8), "a1b2")
        self.assertEqual(truncate_hash(full_hash, 12), "a1b2c3")
        self.assertEqual(truncate_hash(full_hash, 16), "a1b2c3d4")

    def test_get_hash(self):
        h8 = get_hash("test", 8)
        h12 = get_hash("test", 12)
        h16 = get_hash("test", 16)

        self.assertEqual(len(h8), 2)
        self.assertEqual(len(h12), 3)
        self.assertEqual(len(h16), 4)

        self.assertNotEqual(h8, h12)
        self.assertNotEqual(h8, h16)
        self.assertNotEqual(h12, h16)


class TestAttack(unittest.TestCase):
    """Тесты для атаки поиска коллизий."""

    def test_find_collision_8bit(self):
        str1, str2, attempts, _ = find_collision(8, max_attempts=1000)

        self.assertIsNotNone(str1)
        self.assertIsNotNone(str2)
        self.assertNotEqual(str1, str2)
        self.assertEqual(get_hash(str1, 8), get_hash(str2, 8))
        self.assertLess(attempts, 500)

    def test_find_collision_12bit(self):
        str1, str2, attempts, _ = find_collision(12, max_attempts=5000)

        self.assertIsNotNone(str1)
        self.assertIsNotNone(str2)
        self.assertNotEqual(str1, str2)
        self.assertEqual(get_hash(str1, 12), get_hash(str2, 12))

    def test_find_collision_16bit(self):
        str1, str2, attempts, _ = find_collision(16, max_attempts=20000)

        self.assertIsNotNone(str1)
        self.assertIsNotNone(str2)
        self.assertNotEqual(str1, str2)
        self.assertEqual(get_hash(str1, 16), get_hash(str2, 16))

    def test_expected_attempts(self):
        expected_8 = get_expected_attempts(8)
        expected_12 = get_expected_attempts(12)
        expected_16 = get_expected_attempts(16)

        self.assertLess(expected_8, expected_12)
        self.assertLess(expected_12, expected_16)
        self.assertAlmostEqual(expected_8, 20, delta=10)
        self.assertAlmostEqual(expected_12, 80, delta=20)
        self.assertAlmostEqual(expected_16, 320, delta=50)


if __name__ == "__main__":
    unittest.main()