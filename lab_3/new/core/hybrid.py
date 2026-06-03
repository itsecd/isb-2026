from utils.file_utils import read_bytes, write_bytes
from crypto import symmetric, asymmetric


def generate_keys(enc_key_path, pub_path, priv_path):
    try:
        sym_key = symmetric.generate_key()
        private, public = asymmetric.generate_keys()

        enc_key = asymmetric.encrypt_key(public, sym_key)

        write_bytes(priv_path, asymmetric.save_private(private))
        write_bytes(pub_path, asymmetric.save_public(public))
        write_bytes(enc_key_path, enc_key)

    except Exception as e:
        raise RuntimeError(f"[HYBRID ERROR] generate_keys: {e}")


def encrypt_file(input_path, priv_path, enc_key_path, output_path):
    try:
        private = asymmetric.load_private(read_bytes(priv_path))
        enc_key = read_bytes(enc_key_path)

        sym_key = asymmetric.decrypt_key(private, enc_key)

        data = read_bytes(input_path)

        iv, cipher = symmetric.encrypt(sym_key, data)

        write_bytes(output_path, iv + cipher)

    except Exception as e:
        raise RuntimeError(f"[HYBRID ERROR] encrypt_file: {e}")


def decrypt_file(input_path, priv_path, enc_key_path, output_path):
    try:
        private = asymmetric.load_private(read_bytes(priv_path))
        enc_key = read_bytes(enc_key_path)

        sym_key = asymmetric.decrypt_key(private, enc_key)

        data = read_bytes(input_path)

        iv = data[:8]
        cipher = data[8:]

        plain = symmetric.decrypt(sym_key, iv, cipher)

        write_bytes(output_path, plain)

    except Exception as e:
        raise RuntimeError(f"[HYBRID ERROR] decrypt_file: {e}")
