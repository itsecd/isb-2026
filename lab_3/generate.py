import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa

def generate_key(
    path_symmetric_key: str,
    path_asymmetric_public_key: str,
    path_asymmetric_private_key: str,
) -> None:
    symmetric_key = os.urandom(16)

    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()

    with open(path_asymmetric_public_key, "wb") as public_out:
        public_out.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    with open(path_asymmetric_private_key, "wb") as private_out:
        private_out.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    symmetric_key = public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    with open(path_symmetric_key, "wb") as key_file:
        key_file.write(symmetric_key)