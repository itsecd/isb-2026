from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from file_utils import read_binary_file, write_binary_file

class RSAKeyPair:
    def __init__(self, private_key=None, public_key=None):
        if private_key is None:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self.public_key = self.private_key.public_key()
        else:
            self.private_key = private_key
            self.public_key = private_key.public_key()

    @staticmethod
    def load_from_files(priv_path, pub_path):
        with open(priv_path, 'rb') as f:
            priv_bytes = f.read()
        with open(pub_path, 'rb') as f:
            pub_bytes = f.read()
        private_key = serialization.load_pem_private_key(priv_bytes, password=None)
        public_key = serialization.load_pem_public_key(pub_bytes)
        return RSAKeyPair(private_key, public_key)

    def save_to_files(self, priv_path, pub_path):
        pub_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        write_binary_file(pub_path, pub_bytes)
      
        priv_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        write_binary_file(priv_path, priv_bytes)

    def encrypt_symmetric_key(self, symmetric_key):
        return self.public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt_symmetric_key(self, encrypted_symmetric_key):
        return self.private_key.decrypt(
            encrypted_symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
