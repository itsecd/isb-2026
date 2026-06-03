"""Фасад криптографической логики. Взаимодействует с файлами и настройками."""

from typing import Dict
import asymmetric
import symmetric


def generate_hybrid_keys(settings: Dict[str, str], key_size: int) -> str:
    """Координирует создание и экспорт всех ключей гибридной системы."""
    sym_key = symmetric.generate_camellia_key(key_size)

    private_key, public_key = asymmetric.generate_rsa_key_pair()

    with open(settings['public_key'], 'wb') as f:
        f.write(asymmetric.serialize_public_key(public_key))

    with open(settings['secret_key'], 'wb') as f:
        f.write(asymmetric.serialize_private_key(private_key))

    enc_sym_key = asymmetric.encrypt_session_key(public_key, sym_key)
    with open(settings['symmetric_key'], 'wb') as f:
        f.write(enc_sym_key)

    return f"Ключи успешно сгенерированы!\nРазмер Camellia: {key_size} бит."


def encrypt_file_hybrid(settings: Dict[str, str]) -> str:
    """Связывает чтение закрытого RSA ключа и шифрование файла Camellia."""
    with open(settings['secret_key'], 'rb') as f:
        private_key_bytes = f.read()

    with open(settings['symmetric_key'], 'rb') as f:
        enc_sym_key = f.read()
    sym_key = asymmetric.decrypt_session_key(private_key_bytes, enc_sym_key)
    with open(settings['initial_file'], 'rb') as f:
        data = f.read()
    encrypted_blob = symmetric.encrypt_bytes(data, sym_key)
    with open(settings['encrypted_file'], 'wb') as f:
        f.write(encrypted_blob)

    return "Файл успешно зашифрован."


def decrypt_file_hybrid(settings: Dict[str, str]) -> str:
    """Связывает чтение закрытого RSA ключа и дешифрование файла."""
    with open(settings['secret_key'], 'rb') as f:
        private_key_bytes = f.read()

    with open(settings['symmetric_key'], 'rb') as f:
        enc_sym_key = f.read()
    sym_key = asymmetric.decrypt_session_key(private_key_bytes, enc_sym_key)
    with open(settings['encrypted_file'], 'rb') as f:
        file_content = f.read()

    decrypted_data = symmetric.decrypt_bytes(file_content, sym_key)

    with open(settings['decrypted_file'], 'wb') as f:
        f.write(decrypted_data)

    return "Файл успешно расшифрован."