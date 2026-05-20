import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from hmac_core import compute_hmac, verify_hmac


class TestHMACCore(unittest.TestCase):
    def test_compute_hmac_returns_hex(self):
        h = compute_hmac("test", "key")
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 64)  # SHA256 hex = 64 символа

    def test_compute_hmac_different_keys_different_results(self):
        h1 = compute_hmac("hello", "key1")
        h2 = compute_hmac("hello", "key2")
        self.assertNotEqual(h1, h2)

    def test_verify_hmac_correct(self):
        h = compute_hmac("hello", "secret")
        self.assertTrue(verify_hmac("hello", "secret", h))

    def test_verify_hmac_incorrect(self):
        h = compute_hmac("hello", "secret")
        self.assertFalse(verify_hmac("hello", "wrong_key", h))
        self.assertFalse(verify_hmac("hello_changed", "secret", h))

    def test_verify_hmac_empty_strings(self):
        h = compute_hmac("", "")
        self.assertTrue(verify_hmac("", "", h))

    def test_exceptions_invalid_types(self):
        with self.assertRaises(TypeError):
            compute_hmac(123, "key")
        with self.assertRaises(TypeError):
            verify_hmac("msg", 456, "hash")


if __name__ == "__main__":
    unittest.main()