"""
Unit tests for hashing, saving, and verifying files.
"""

import os
import tempfile
import unittest

from hash_utils import sha256_file, save_checksum, verify_file


class TestHashUtils(unittest.TestCase):
    """
    Tests for utility functions in hash_utils.py.
    """

    def test_sha256_hello_world(self):
        """
        Check SHA-256 hash for the exact string 'Hello World'.
        """
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"Hello World")
            path = f.name
        try:
            self.assertEqual(
                sha256_file(path),
                "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
            )
        finally:
            os.remove(path)

    def test_save_and_verify_ok(self):
        """
        Check that verification passes for an unchanged file.
        """
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"abc")
            path = f.name

        try:
            checksum = sha256_file(path)
            checksum_path = save_checksum(path, checksum)
            ok, current, saved = verify_file(path, checksum_path)

            self.assertTrue(ok)
            self.assertEqual(current, saved)
        finally:
            for p in (path, path + ".sha256"):
                if os.path.exists(p):
                    os.remove(p)

    def test_verify_fail_after_change(self):
        """
        Check that verification fails after file modification.
        """
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"abc")
            path = f.name

        try:
            checksum = sha256_file(path)
            checksum_path = save_checksum(path, checksum)

            with open(path, "wb") as f:
                f.write(b"abcd")

            ok, _, _ = verify_file(path, checksum_path)
            self.assertFalse(ok)
        finally:
            for p in (path, path + ".sha256"):
                if os.path.exists(p):
                    os.remove(p)


if __name__ == "__main__":
    unittest.main()