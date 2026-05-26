"""
Unit tests for the file integrity checker.
"""

import os
import tempfile
import unittest

from hash_utils import sha256_file, save_checksum, verify_file


class TestHashUtils(unittest.TestCase):
    """
    Tests for hash utility functions.
    """

    def test_sha256_hello_world(self):
        """
        Check SHA-256 for the string 'Hello World'.
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

    def test_verify_ok_and_fail(self):
        """
        Verify that checksum passes before modification and fails after modification.
        """
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"abc")
            path = f.name

        try:
            checksum = sha256_file(path)
            checksum_path = save_checksum(path, checksum)

            ok, _, _ = verify_file(path, checksum_path)
            self.assertTrue(ok)

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