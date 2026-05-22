import os
from crypto_utils import generate_hash


def test_generate_hash_returns_bytes():
    """Test that generate_hash returns a bytes object of length 32 (SHA256 output)."""
    salt = os.urandom(16)
    result = generate_hash("password", salt)
    assert isinstance(result, bytes)
    assert len(result) == 32


def test_same_password_same_salt_same_hash():
    """Test that identical password and salt produce identical hash."""
    salt = os.urandom(16)
    hash1 = generate_hash("test", salt)
    hash2 = generate_hash("test", salt)
    assert hash1 == hash2


def test_different_salt_different_hash():
    """Test that different salts (even for same password) produce different hashes."""
    salt1 = os.urandom(16)
    salt2 = os.urandom(16)
    hash1 = generate_hash("test", salt1)
    hash2 = generate_hash("test", salt2)
    assert hash1 != hash2


def test_different_password_different_hash():
    """Test that different passwords with the same salt produce different hashes."""
    salt = os.urandom(16)
    hash1 = generate_hash("pass123", salt)
    hash2 = generate_hash("pass456", salt)
    assert hash1 != hash2
