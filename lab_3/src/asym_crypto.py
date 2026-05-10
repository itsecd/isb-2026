from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes

def get_asym_padding():
    """Returns a padding object for the RSA algorithm."""
    try:
        return asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    except Exception as e:
        raise RuntimeError(f"RSA padding configuration error: {e}")

def generate_rsa_keys(public_exponent: int = 65537, key_size: int = 2048) -> tuple[bytes, bytes]:
    """Generating an RSA key pair."""
    try:
        private_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size
        )
        public_key = private_key.public_key()

        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        priv_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        return pub_bytes, priv_bytes
    except Exception as e:
        raise RuntimeError(f"RSA key generation failure: {e}")

def encrypt_rsa(public_key_pem: bytes, data: bytes) -> bytes:
    """Data encryption using a public RSA key."""
    try:
        public_key = serialization.load_pem_public_key(public_key_pem)
        return public_key.encrypt(data, get_asym_padding())
    except Exception as e:
        raise RuntimeError(f"RSA encryption error: {e}")

def decrypt_rsa(private_key_pem: bytes, encrypted_data: bytes) -> bytes:
    """Decryption of data using a private RSA key."""
    try:
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        return private_key.decrypt(encrypted_data, get_asym_padding())
    except Exception as e:
        raise RuntimeError(f"RSA decryption error: {e}")