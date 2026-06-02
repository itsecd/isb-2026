import unittest

from collisions import find_single_collision
from hash_utils import generate_string, get_short_hash


class TestHashApp(unittest.TestCase):

    def test_generate_string(self):
        """
        Checking the length and randomness of string generation.
        """
        s1 = generate_string(16)
        s2 = generate_string(16)
        self.assertEqual(len(s1), 16)
        self.assertNotEqual(s1, s2)

    def test_get_short_cash_validity(self):
        """
        We verify that the truncated hash falls within the correct mathematical bounds.
        """
        test_str = "random"

        h8 = get_short_hash(test_str, 8)
        self.assertTrue(0 <= h8 <= 255)  # 2^8 - 1

        h12 = get_short_hash(test_str, 12)
        self.assertTrue(0 <= h12 <= 4095)  # 2^12 - 1

        h16 = get_short_hash(test_str, 16)
        self.assertTrue(0 <= h16 <= 65535)  # 2^16 - 1

    def test_get_short_cash_invalid_length(self):
        """
        Checking the response to an incorrect length (ValueError)
        """
        with self.assertRaises(ValueError):
            get_short_hash("test", 10)

    def test_find_single_collision(self):
        """
        We verify that the returned strings are different, but the hashes are identical.
        """
        s1, s2, h_val, attempts = find_single_collision(8)

        self.assertNotEqual(s1, s2)
        self.assertGreater(attempts, 0)

        self.assertEqual(get_short_hash(s1, 8), get_short_hash(s2, 8))
        self.assertEqual(get_short_hash(s1, 8), h_val)


if __name__ == '__main__':
    unittest.main()
