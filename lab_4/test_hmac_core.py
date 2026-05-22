import pytest

from hmac_core import generate_hmac, verify_hmac


def test_generate_hmac_returns_string():
    mac = generate_hmac("Hello", "secret")

    assert isinstance(mac, str)


def test_hmac_sha256_length_is_64():
    mac = generate_hmac("Hello", "secret")

    assert len(mac) == 64


def test_verify_correct_hmac():
    message = "Hello"
    key = "secret"
    mac = generate_hmac(message, key)

    assert verify_hmac(message, key, mac) is True


def test_detect_modified_message():
    message = "Hello"
    key = "secret"
    mac = generate_hmac(message, key)

    assert verify_hmac("Hello hacked", key, mac) is False


def test_detect_wrong_key():
    message = "Hello"
    correct_key = "secret"
    wrong_key = "wrong_secret"

    mac = generate_hmac(message, correct_key)

    assert verify_hmac(message, wrong_key, mac) is False


def test_empty_input_raises_error():
    with pytest.raises(ValueError):
        generate_hmac("", "secret")

    with pytest.raises(ValueError):
        generate_hmac("Hello", "")

    with pytest.raises(ValueError):
        verify_hmac("Hello", "secret", "")