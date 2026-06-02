import pytest
from l4 import (
    generate_random_string,
    hash_string,
    cut_hash,
    find_collision,
    create_dict_csv,
    append_to_csv,
    read_csv,
    stats_from_csv,
)

def test_generate_random_string_length():
    result = generate_random_string(10)
    assert isinstance(result, str)
    assert len(result) == 10


def test_generate_random_string_invalid_length():
    with pytest.raises(ValueError):
        generate_random_string(0)


def test_hash_string_is_deterministic():
    assert hash_string("test") == hash_string("test")


def test_hash_string_length():
    result = hash_string("test")
    assert len(result) == 64


def test_cut_hash_8_bits():
    full_hash = "abcdef123456"
    assert cut_hash(full_hash, 8) == "ab"


def test_cut_hash_12_bits():
    full_hash = "abcdef123456"
    assert cut_hash(full_hash, 12) == "abc"


def test_cut_hash_16_bits():
    full_hash = "abcdef123456"
    assert cut_hash(full_hash, 16) == "abcd"


def test_cut_hash_invalid_bits():
    with pytest.raises(ValueError):
        cut_hash("abcdef", 10)


def test_find_collision_returns_valid_collision():
    result = find_collision(length=10, bits=8)
    assert result["string1"] != result["string2"]
    assert result["attempts"] > 0
    hash1 = cut_hash(hash_string(result["string1"]), 8)
    hash2 = cut_hash(hash_string(result["string2"]), 8)
    assert hash1 == hash2
    assert hash1 == result["hash"]


def test_csv_create_append_read(tmp_path):
    file_path = tmp_path / "test.csv"
    fieldnames = ["experiment", "bits", "hash", "string1", "string2", "attempts"]
    create_dict_csv(str(file_path), fieldnames)
    row = {
        "experiment": 1,
        "bits": 8,
        "hash": "ab",
        "string1": "AAAA",
        "string2": "BBBB",
        "attempts": 20
    }
    append_to_csv(str(file_path), row, fieldnames)
    data = read_csv(str(file_path))
    assert len(data) == 1
    assert data[0]["bits"] == "8"
    assert data[0]["hash"] == "ab"
    assert data[0]["attempts"] == "20"


def test_stats_from_csv(tmp_path):
    file_path = tmp_path / "collisions.csv"
    fieldnames = ["experiment", "bits", "hash", "string1", "string2", "attempts"]
    create_dict_csv(str(file_path), fieldnames)
    rows = [
        {"experiment": 1, "bits": 8, "hash": "aa", "string1": "a", "string2": "b", "attempts": 10},
        {"experiment": 2, "bits": 8, "hash": "bb", "string1": "c", "string2": "d", "attempts": 20},
        {"experiment": 1, "bits": 12, "hash": "abc", "string1": "e", "string2": "f", "attempts": 60},
        {"experiment": 2, "bits": 12, "hash": "def", "string1": "g", "string2": "h", "attempts": 80},
    ]
    for row in rows:
        append_to_csv(str(file_path), row, fieldnames)
    stats = stats_from_csv(str(file_path))
    stats_by_bits = {row["bits"]: row for row in stats}
    assert stats_by_bits[8]["experiments"] == 2
    assert stats_by_bits[8]["average_attempts"] == 15
    assert stats_by_bits[8]["min_attempts"] == 10
    assert stats_by_bits[8]["max_attempts"] == 20
    assert stats_by_bits[12]["experiments"] == 2
    assert stats_by_bits[12]["average_attempts"] == 70