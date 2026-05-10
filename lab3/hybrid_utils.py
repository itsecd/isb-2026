import os
from des3_utils import generate_key as gen_3des, pad_data, unpad_data, encrypt as enc_3des, decrypt as dec_3des
from rsa_utils import generate_keys, save_private_key, save_public_key, load_public_key, load_private_key, encrypt_key, decrypt_key


def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_file(path: str, data: bytes):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def generate_all_keys(enc_key_path: str, pub_path: str, priv_path: str, key_size: int):
    des3_key = gen_3des(key_size)
    private_key, public_key = generate_keys()

    save_private_key(private_key, priv_path)
    save_public_key(public_key, pub_path)

    encrypted_des3_key = encrypt_key(des3_key, public_key)
    write_file(enc_key_path, encrypted_des3_key)


def encrypt_file(input_path: str, pub_key_path: str, enc_key_path: str, output_path: str):
    public_key = load_public_key(pub_key_path)
    des3_key = gen_3des()

    encrypted_des3_key = encrypt_key(des3_key, public_key)
    write_file(enc_key_path, encrypted_des3_key)

    data = read_file(input_path)
    padded = pad_data(data)
    iv, encrypted = enc_3des(padded, des3_key)
    write_file(output_path, iv + encrypted)


def decrypt_file(input_path: str, priv_key_path: str, enc_key_path: str, output_path: str):
    private_key = load_private_key(priv_key_path)
    encrypted_des3_key = read_file(enc_key_path)
    des3_key = decrypt_key(encrypted_des3_key, private_key)

    data = read_file(input_path)
    iv = data[:8]
    encrypted = data[8:]

    decrypted_padded = dec_3des(encrypted, des3_key, iv)
    decrypted = unpad_data(decrypted_padded)
    write_file(output_path, decrypted)