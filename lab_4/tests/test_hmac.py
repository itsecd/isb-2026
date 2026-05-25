# -*- coding: utf-8 -*-
"""Unit tests for HMACTask — modules/hmac_core.py and modules/collision.py."""

import json
import os
import tempfile
import unittest

import modules.hmac_core as hmac_core
import modules.collision as collision


class TestComputeHmac(unittest.TestCase):
    """Tests for :func:`hmac_core.compute_hmac`."""

    def test_returns_hex_string(self) -> None:
        """Return value must be a non-empty hex string."""
        result = hmac_core.compute_hmac("hello", "secret")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Must be valid hex.
        int(result, 16)

    def test_deterministic(self) -> None:
        """Same inputs must always produce the same HMAC."""
        tag1 = hmac_core.compute_hmac("hello", "secret")
        tag2 = hmac_core.compute_hmac("hello", "secret")
        self.assertEqual(tag1, tag2)

    def test_different_messages_differ(self) -> None:
        """Different messages must produce different HMACs."""
        tag1 = hmac_core.compute_hmac("hello", "secret")
        tag2 = hmac_core.compute_hmac("world", "secret")
        self.assertNotEqual(tag1, tag2)

    def test_different_keys_differ(self) -> None:
        """Different keys must produce different HMACs for the same message."""
        tag1 = hmac_core.compute_hmac("hello", "key1")
        tag2 = hmac_core.compute_hmac("hello", "key2")
        self.assertNotEqual(tag1, tag2)

    def test_sha512_produces_longer_tag(self) -> None:
        """SHA-512 digest must be longer than SHA-256 digest."""
        tag256 = hmac_core.compute_hmac("msg", "k", algo="sha256")
        tag512 = hmac_core.compute_hmac("msg", "k", algo="sha512")
        self.assertGreater(len(tag512), len(tag256))

    def test_unsupported_algo_raises(self) -> None:
        """Unsupported algorithm must raise :exc:`ValueError`."""
        with self.assertRaises(ValueError):
            hmac_core.compute_hmac("msg", "key", algo="md5")

    def test_non_string_raises(self) -> None:
        """Non-string inputs must raise :exc:`TypeError`."""
        with self.assertRaises(TypeError):
            hmac_core.compute_hmac(123, "key")  # type: ignore[arg-type]


class TestVerifyHmac(unittest.TestCase):
    """Tests for :func:`hmac_core.verify_hmac`."""

    def test_valid_tag_passes(self) -> None:
        """Correct tag must return ``True``."""
        tag = hmac_core.compute_hmac("test message", "mykey")
        self.assertTrue(hmac_core.verify_hmac("test message", "mykey", tag))

    def test_wrong_message_fails(self) -> None:
        """Modified message must return ``False``."""
        tag = hmac_core.compute_hmac("original", "mykey")
        self.assertFalse(hmac_core.verify_hmac("tampered", "mykey", tag))

    def test_wrong_key_fails(self) -> None:
        """Wrong key must return ``False``."""
        tag = hmac_core.compute_hmac("msg", "correct_key")
        self.assertFalse(hmac_core.verify_hmac("msg", "wrong_key", tag))

    def test_corrupted_tag_fails(self) -> None:
        """Corrupted tag must return ``False``."""
        tag = hmac_core.compute_hmac("msg", "key")
        bad_tag = tag[:-4] + "0000"
        self.assertFalse(hmac_core.verify_hmac("msg", "key", bad_tag))


class TestSignAndSave(unittest.TestCase):
    """Tests for :func:`hmac_core.sign_and_save`."""

    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self) -> None:
        os.unlink(self.path)

    def test_file_created(self) -> None:
        """Output file must be created."""
        hmac_core.sign_and_save("hello", "secret", self.path)
        self.assertTrue(os.path.exists(self.path))

    def test_envelope_structure(self) -> None:
        """Saved JSON must contain message, hmac, and algo fields."""
        hmac_core.sign_and_save("hello", "secret", self.path)
        with open(self.path, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertIn("message", data)
        self.assertIn("hmac", data)
        self.assertIn("algo", data)

    def test_envelope_message_matches(self) -> None:
        """Saved message must equal the original."""
        hmac_core.sign_and_save("hello world", "secret", self.path)
        with open(self.path, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(data["message"], "hello world")


class TestLoadAndVerify(unittest.TestCase):
    """Tests for :func:`hmac_core.load_and_verify`."""

    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self) -> None:
        os.unlink(self.path)

    def test_valid_envelope_passes(self) -> None:
        """A correctly signed envelope must verify as ``True``."""
        hmac_core.sign_and_save("secure message", "k3y!", self.path)
        is_valid, _ = hmac_core.load_and_verify(self.path, "k3y!")
        self.assertTrue(is_valid)

    def test_wrong_key_fails(self) -> None:
        """Wrong key must make verification return ``False``."""
        hmac_core.sign_and_save("secure message", "correct", self.path)
        is_valid, _ = hmac_core.load_and_verify(self.path, "wrong")
        self.assertFalse(is_valid)

    def test_missing_file_raises(self) -> None:
        """Non-existent file must raise :exc:`FileNotFoundError`."""
        with self.assertRaises(FileNotFoundError):
            hmac_core.load_and_verify("/nonexistent/path.json", "key")


class TestTamperAndVerify(unittest.TestCase):
    """Tests for :func:`hmac_core.tamper_and_verify`."""

    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.path = self.tmp.name
        hmac_core.sign_and_save("original message", "secret", self.path)

    def tearDown(self) -> None:
        os.unlink(self.path)

    def test_tampered_message_rejected(self) -> None:
        """Tampered message must return ``False``."""
        result = hmac_core.tamper_and_verify(self.path, "secret", "modified message")
        self.assertFalse(result)

    def test_original_message_accepted(self) -> None:
        """Original message passed as tampered must still return ``True``."""
        result = hmac_core.tamper_and_verify(self.path, "secret", "original message")
        self.assertTrue(result)


class TestCollision(unittest.TestCase):
    """Tests for :func:`collision.find_partial_collision`."""

    def test_finds_collision_with_small_prefix(self) -> None:
        """8-bit prefix collision must be found quickly."""
        result = collision.find_partial_collision("testkey", prefix_bits=8, max_attempts=50_000)
        self.assertIsNotNone(result)
        msg_a, msg_b, prefix = result  # type: ignore[misc]
        self.assertNotEqual(msg_a, msg_b)
        self.assertTrue(prefix.startswith("0x"))

    def test_returns_none_on_zero_attempts(self) -> None:
        """Zero attempts must always return ``None``."""
        result = collision.find_partial_collision("key", prefix_bits=8, max_attempts=0)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
