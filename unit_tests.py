import os
import pytest

import database
import hash
import without_salt


def test_init_database():
    """Проверяет создание файла базы данных."""
    database.init_database("test.db")
    assert os.path.exists("test.db")

def test_add_user_and_get():
    """Проверяет добавление пользователя в БД и корректность извлечения его данных."""
    database.add_user("test.db","blub","password1","salt1")
    result = database.get_data("test.db", "blub")
    assert result[0][0]=="password1"
    assert result[0][1]=="salt1"

def test_get_unknown_user():
    """Проверяет, что запрос несуществующего пользователя возвращает пустой список."""
    result = database.get_data("test.db", "unknown")
    assert result == []

def test_hash():
    """
    Тестирует хеширование с солью (bcrypt)
    """
    pas="password"
    hash_,salt=hash.generate_hash(pas)
    assert hash.check_password(hash_,pas) is True
    assert hash.check_password(hash_,"oasd") is False

def test_without_salt():
    """
    Тестирует хеширование без соли (SHA-256):
    """
    pas="password"
    hash_=without_salt.hash_without_salt(pas)
    assert without_salt.check_password_w(pas,hash_) is True
    assert without_salt.check_password_w("passwor",hash_) is False

@pytest.fixture(autouse=True, scope="module")
def clean():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
