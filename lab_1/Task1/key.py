from Ru import ALPHABET, ALPHABET_LEN


SHIFT = 10


def generate_encrypt_key(shift=SHIFT):
    """Генерирует ключ для шифрования шифром Цезаря"""
    encrypt_key = {}

    for i, original_char in enumerate(ALPHABET):
        encrypted_index = (i + shift) % ALPHABET_LEN
        encrypted_char = ALPHABET[encrypted_index]
        encrypt_key[original_char] = encrypted_char

    return encrypt_key


def generate_decrypt_key(shift=SHIFT):
    """Генерирует ключ для расшифровки шифра Цезаря"""
    encrypt_key = generate_encrypt_key(shift)
    decrypt_key = {}

    for original_char, encrypted_char in encrypt_key.items():
        decrypt_key[encrypted_char] = original_char

    return decrypt_key


encrypt_key = generate_encrypt_key()
decrypt_key = generate_decrypt_key()
