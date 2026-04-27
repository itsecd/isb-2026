from crypto_core import (
    create_symmetric_key,
    create_initial_vector,
    _read_binary_file,
    _write_binary_file,
    symmetric_encrypt,
    symmetric_decrypt,
    load_public_key,
    load_private_key,
    asymmetric_encrypt,
    asymmetric_decrypt
)


def prepare_encrypted_package(input_file: str, output_file: str, public_key_path: str,
                              key_size: int = 16, iv_size: int = 16, block_size_bits: int = 128) -> None:
    """Генерация ключей для SEED, симметричное шифрование, шифрования генерированного
    ключа через принцип RSA, запись в файл"""
    sym_key = create_symmetric_key(key_size)
    iv = create_initial_vector(iv_size)
    plain_data = _read_binary_file(input_file)
    encrypted_data = symmetric_encrypt(sym_key, iv, plain_data, block_size_bits)
    public_key = load_public_key(public_key_path)
    encrypted_key = asymmetric_encrypt(sym_key, public_key)
    _write_binary_file(output_file, 
        len(encrypted_key).to_bytes(4, 'big') + encrypted_key + iv + encrypted_data)


def extract_decrypted_package(encrypted_file: str, output_file: str, private_key_path: str,
                              iv_size: int = 16, block_size_bits: int = 128) -> None:
    """Считывание данных из бинарного файла, расшифровка ключа через RSA, расшифровка 
    симметричным дешифрованием"""
    data = _read_binary_file(encrypted_file)
    key_len = int.from_bytes(data[:4], 'big')
    encrypted_key = data[4:4+key_len]
    iv = data[4+key_len:4+key_len+iv_size]
    ciphertext = data[4+key_len+iv_size:]
    private_key = load_private_key(private_key_path)
    sym_key = asymmetric_decrypt(encrypted_key, private_key)
    plain_data = symmetric_decrypt(sym_key, iv, ciphertext, block_size_bits)
    _write_binary_file(output_file, plain_data)