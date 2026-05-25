"""
Набор unit-тестов для проверки HMAC.
"""

import unittest

from crypto_engine import build_hmac, check_hmac


class HmacTests(unittest.TestCase):
    def test_hmac_length(self):

        result = build_hmac("hello", "key")

        self.assertEqual(len(result), 64)

    def test_different_keys(self):

        first = build_hmac("hello", "key1")

        second = build_hmac("hello", "key2")

        self.assertNotEqual(first, second)

    def test_valid_signature(self):

        signature = build_hmac("data", "secret")

        self.assertTrue(check_hmac("data", "secret", signature))

    def test_invalid_signature(self):

        signature = build_hmac("data", "secret")

        self.assertFalse(check_hmac("changed", "secret", signature))

    def test_invalid_types(self):

        with self.assertRaises(TypeError):
            build_hmac(123, "key")


if __name__ == "__main__":
    unittest.main()
