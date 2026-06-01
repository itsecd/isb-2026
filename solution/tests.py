import json
import pytest

import main


def test_create_hmac():
    h1 = main.create_hmac("key", "hello")
    h2 = main.create_hmac("key", "hello")
    h3 = main.create_hmac("key", "hollo")
    assert h1 == h2
    assert h1 != h3
    assert len(h1) == 64


def test_verify_hmac():
    key = "key"
    data = "hello"
    h = main.create_hmac(key, data)

    assert main.verify_hmac(key, data, h) is True
    assert main.verify_hmac(key, "hollo", h) is False


def test_send_and_receive_message(tmp_path):
    key = "secret"
    data = "hello"
    h = main.create_hmac(key, data)

    p = tmp_path / "msg.json"
    main.send_message(data, h, str(p))

    received = json.loads(p.read_text(encoding="utf-8"))
    assert received["data"] == data
    assert received["hmac_hash"] == h

    assert main.receive_message(key, str(p)) is True


def test_read_data_missing_returns_empty(tmp_path):
    assert main.read_data(str(tmp_path / "missing.txt")) == ""


def test_write_data_and_read_back(tmp_path):
    path = tmp_path / "a.txt"
    main.write_data("abc", str(path))
    assert main.read_data(str(path)) == "abc"