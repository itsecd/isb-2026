from symmetric import SymmetricCipher
from asymmetric import AsymmetricCipher
from file_utils import FileService

class HybridCryptoSystem:
    """Оркестратор для реализации комплексных сценариев работы гибридной криптосистемы."""

    def __init__(self):
        self._file_service = FileService()

    def run_key_generation(
        self,
        encrypted_key_path: str,
        public_key_path: str,
        private_key_path: str,
        aes_key_size: int,
        rsa_key_size: int,
        rsa_public_exponent: int,
    ) -> None:
        sym = SymmetricCipher(aes_key_size)
        asym = AsymmetricCipher(rsa_key_size, rsa_public_exponent)

        aes_key = sym.generate_key()
        priv_key, pub_key = asym.generate_pair()

        self._file_service.write_bytes(public_key_path, asym.serialize_public_key(pub_key))
        self._file_service.write_bytes(private_key_path, asym.serialize_private_key(priv_key))

        enc_aes_key = asym.encrypt_session_key(aes_key, pub_key)
        self._file_service.write_bytes(encrypted_key_path, enc_aes_key)

    def run_encryption(
        self, input_path: str, private_key_path: str, encrypted_key_path: str, output_path: str
    ) -> None:
        asym = AsymmetricCipher()
        sym = SymmetricCipher()

        priv_bytes = self._file_service.read_bytes(private_key_path)
        priv_key = asym.load_private_key(priv_bytes)

        enc_key_bytes = self._file_service.read_bytes(encrypted_key_path)
        aes_key = asym.decrypt_session_key(enc_key_bytes, priv_key)

        source_data = self._file_service.read_bytes(input_path)
        encrypted_data = sym.encrypt(source_data, aes_key)
        self._file_service.write_bytes(output_path, encrypted_data)

    def run_decryption(
        self, input_path: str, private_key_path: str, encrypted_key_path: str, output_path: str
    ) -> None:
        asym = AsymmetricCipher()
        sym = SymmetricCipher()

        priv_bytes = self._file_service.read_bytes(private_key_path)
        priv_key = asym.load_private_key(priv_bytes)

        enc_key_bytes = self._file_service.read_bytes(encrypted_key_path)
        aes_key = asym.decrypt_session_key(enc_key_bytes, priv_key)

        encrypted_data = self._file_service.read_bytes(input_path)
        decrypted_data = sym.decrypt(encrypted_data, aes_key)
        self._file_service.write_bytes(output_path, decrypted_data)