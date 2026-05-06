import os

def read_binary_file(path):
    with open(path, 'rb') as f:
        return f.read()

def write_binary_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def read_text_file(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        return f.read()

def write_text_file(path, text, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        f.write(text)

def generate_random_bytes(n):
    return os.urandom(n)
