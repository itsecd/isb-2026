"""Фасад криптографической логики. Взаимодействует с файлами через file_io."""

from typing import Dict
import asymmetric
import symmetric
import file_io


def generate_hybrid_keys(settings: Dict[str, str], key_size_bits: int) -> str:
    """Генерирует и сохраняет все ключи гибридной системы.

    Args:
        settings: Словарь с настройками. Ожидаются ключи:
            'public_key', 'secret_key', 'symmetric_key'.
        key_size_bits: Размер симметричного ключа в битах (128, 192 или 256).

    Returns:
        str: Сообщение об успешной генерации.
    """
    sym_key = symmetric.generate_camellia_key(key_size_bits)

    private_key, public_key = asymmetric.generate_rsa_key_pair()
    file_io.write_bytes(settings['public_key'], asymmetric.serialize_public_key(public_key))
    file_io.write_bytes(settings['secret_key'], asymmetric.serialize_private_key(private_key))

    enc_sym_key = asymmetric.encrypt_session_key(public_key, sym_key)
    file_io.write_bytes(settings['symmetric_key'], enc_sym_key)

    return f"Ключи успешно сгенерированы!\nРазмер Camellia: {key_size_bits} бит."


def encrypt_file_hybrid(settings: Dict[str, str]) -> str:
    """Шифрует исходный файл, используя сохранённый сеансовый ключ.

    Args:
        settings: Словарь с настройками. Ожидаются ключи:
            'secret_key', 'symmetric_key', 'initial_file', 'encrypted_file',
            'camellia_block_size_bits', 'camellia_block_size_bytes'.

    Returns:
        str: Сообщение об успешном шифровании.
    """
    private_key_bytes = file_io.read_bytes(settings['secret_key'])
    enc_sym_key = file_io.read_bytes(settings['symmetric_key'])
    sym_key = asymmetric.decrypt_session_key(private_key_bytes, enc_sym_key)

    data = file_io.read_bytes(settings['initial_file'])
    block_bits = int(settings['camellia_block_size_bits'])
    block_bytes = int(settings['camellia_block_size_bytes'])
    encrypted_blob = symmetric.encrypt_bytes(data, sym_key, block_bits, block_bytes)

    file_io.write_bytes(settings['encrypted_file'], encrypted_blob)
    return "Файл успешно зашифрован."


def decrypt_file_hybrid(settings: Dict[str, str]) -> str:
    """Расшифровывает файл, используя сохранённый сеансовый ключ.

    Args:
        settings: Словарь с настройками. Ожидаются ключи:
            'secret_key', 'symmetric_key', 'encrypted_file', 'decrypted_file',
            'camellia_block_size_bits', 'camellia_block_size_bytes'.

    Returns:
        str: Сообщение об успешном дешифровании.
    """
    private_key_bytes = file_io.read_bytes(settings['secret_key'])
    enc_sym_key = file_io.read_bytes(settings['symmetric_key'])
    sym_key = asymmetric.decrypt_session_key(private_key_bytes, enc_sym_key)

    file_content = file_io.read_bytes(settings['encrypted_file'])
    block_bits = int(settings['camellia_block_size_bits'])
    block_bytes = int(settings['camellia_block_size_bytes'])
    decrypted_data = symmetric.decrypt_bytes(file_content, sym_key, block_bits, block_bytes)

    file_io.write_bytes(settings['decrypted_file'], decrypted_data)
    return "Файл успешно расшифрован."
