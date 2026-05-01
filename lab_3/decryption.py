from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def decrypt(
    path_cipher_text: str,
    path_asymmetric_private_text: str,
    path_symmetric_key: str,
    path_original_text: str,
) -> None:
    with open(path_symmetric_key, mode="rb") as key_file:
        symmetric_key = key_file.read()

    with open(path_asymmetric_private_text, "rb") as pem_in:
        private_bytes = pem_in.read()
        private_key = load_pem_private_key(
            private_bytes,
            password=None,
        )

    symmetric_key = private_key.decrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    with open(path_cipher_text, "rb") as f:
        data = f.read()

    iv = data[:16]
    c_text = data[16:]

    cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    c_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    unpadded_c_text = unpadder.update(c_text) + unpadder.finalize()

    with open(path_original_text, "wb") as f:
        f.write(unpadded_c_text)