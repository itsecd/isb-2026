from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes

def get_asym_padding():
    """Returns a padding object for the RSA algorithm.
    Returns:
         asym_padding.AOEP: padded asymmetric object.
    Raises:
        Runtime error: if an unexpected error occurs.
    """
    try:
        return asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    except Exception as e:
        raise RuntimeError(f"RSA padding configuration error: {e}")

def generate_rsa_keys(public_exponent: int, key_size: int) -> tuple[bytes, bytes]:
    """Generating an RSA key pair.
        Args:
            public_exponent: Public exponent of the RSA key to use.
            key_size: Size of the key to use.
        Returns:
            tuple[bytes, bytes]
        Raises:
            Runtime error: if key generation or serialization fails.
    """
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
    """Data encryption using a public RSA key.
        Args:
            public_key_pem (bytes): RSA public key to use.
            data (bytes): Data to encrypt.
        Returns:
            bytes: Encrypted data.
        Raises:
            Runtime error: if encryption fails.
    """
    try:
        public_key = serialization.load_pem_public_key(public_key_pem)
        return public_key.encrypt(data, get_asym_padding())
    except Exception as e:
        raise RuntimeError(f"RSA encryption error: {e}")

def decrypt_rsa(private_key_pem: bytes, encrypted_data: bytes) -> bytes:
    """Decryption of data using a private RSA key.
        Args:
            private_key_pem (bytes): RSA private key to use.
            encrypted_data (bytes): Data to decrypt.
        Returns:
            bytes: Encrypted data.
        Raises:
            Runtime error: if decryption fails.
    """
    try:
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        return private_key.decrypt(encrypted_data, get_asym_padding())
    except Exception as e:
        raise RuntimeError(f"RSA decryption error: {e}")