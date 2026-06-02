import unittest

from collisions import find_single_collision
from hash_utils import generate_string, get_short_hash


class TestHashApp(unittest.TestCase):

    def test_generate_string_default(self):
        """
        Checking the length and randomness of string generation with default parameters.
        """
        s1 = generate_string(16)
        s2 = generate_string(16)
        self.assertEqual(len(s1), 16)
        self.assertNotEqual(s1, s2)

    def test_generate_string_custom_length(self):
        """
        Checking the generation of strings with custom and edge-case lengths.
        """
        s_short = generate_string(5)
        s_long = generate_string(100)
        s_empty = generate_string(0)

        self.assertEqual(len(s_short), 5)
        self.assertEqual(len(s_long), 100)
        self.assertEqual(len(s_empty), 0)

    def test_get_short_hash_validity(self):
        """
        Verify that the truncated hash falls within the correct mathematical bounds.
        """
        test_str = "random"

        h8 = get_short_hash(test_str, 8)
        self.assertTrue(0 <= h8 <= 255)  # 2^8 - 1

        h12 = get_short_hash(test_str, 12)
        self.assertTrue(0 <= h12 <= 4095)  # 2^12 - 1

        h16 = get_short_hash(test_str, 16)
        self.assertTrue(0 <= h16 <= 65535)  # 2^16 - 1

    def test_get_short_hash_determinism(self):
        """
        We verify that hashing the exact same string multiple times yields the exact same result.
        """
        test_str = "determinism_test_string"
        hash1 = get_short_hash(test_str, 16)
        hash2 = get_short_hash(test_str, 16)

        self.assertEqual(hash1, hash2)

    def test_get_short_hash_different_strings(self):
        """
        Checking that completely different strings produce different hashes.
        (Collision probability for 16 bits on just 2 strings is 1/65536, which is practically zero).
        """
        hash1 = get_short_hash("string_number_one", 16)
        hash2 = get_short_hash("string_number_two", 16)

        self.assertNotEqual(hash1, hash2)

    def test_get_short_hash_empty_string(self):
        """
        Checking that an empty string is hashed correctly without raising any errors.
        """
        h8 = get_short_hash("", 8)
        h16 = get_short_hash("", 16)

        self.assertTrue(0 <= h8 <= 255)
        self.assertTrue(0 <= h16 <= 65535)

    def test_get_short_hash_invalid_length(self):
        """
        Checking the response to an incorrect length (ValueError).
        """
        with self.assertRaises(ValueError):
            get_short_hash("test", 10)

        with self.assertRaises(ValueError):
            get_short_hash("test", 24)

    def test_get_short_hash_negative_length(self):
        """
        Checking the response to negative length values and zero (ValueError).
        """
        with self.assertRaises(ValueError):
            get_short_hash("test", -8)

        with self.assertRaises(ValueError):
            get_short_hash("test", 0)

    def test_find_single_collision_8_bits(self):
        """
        Verify that the returned strings are different, but the hashes are identical (for 8 bits).
        """
        s1, s2, h_val, attempts = find_single_collision(8)

        self.assertNotEqual(s1, s2)
        self.assertGreater(attempts, 0)

        self.assertEqual(get_short_hash(s1, 8), get_short_hash(s2, 8))
        self.assertEqual(get_short_hash(s1, 8), h_val)

    def test_find_single_collision_12_bits(self):
        """
        Verify that the collision algorithm scales and correctly finds a collision for 12 bits.
        """
        s1, s2, h_val, attempts = find_single_collision(12)

        self.assertNotEqual(s1, s2)
        self.assertGreater(attempts, 0)

        self.assertEqual(get_short_hash(s1, 12), get_short_hash(s2, 12))
        self.assertEqual(get_short_hash(s1, 12), h_val)


if __name__ == '__main__':
    unittest.main()
