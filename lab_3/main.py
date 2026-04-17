import argparse
import os
import json

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes



def load_settings(config_path: str = 'settings.json') -> dict:
    """Loads the settings from a JSON file."""
    print(f"--Reading the configuration from {config_path}...")
    with open(config_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def get_asym_padding():
    """Returns a padding object for the RSA algorithm."""
    return asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )


def generate_keys(settings: dict):
    """Hybrid system key generation."""
    print("\n!!STARTING KEY GENERATION!!")

    print("-Generating a 128-bit key for the SEED algorithm...")
    sym_key = os.urandom(16)

    print("-Generating an RSA key pair...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    print(f"-Saving the public key in {settings['public_key']}...")
    with open(settings['public_key'], 'wb') as pub_out:
        pub_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"-Saving the private key in {settings['secret_key']}...")
    with open(settings['secret_key'], 'wb') as priv_out:
        priv_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    print(f"-Symmetric key encryption and storage in {settings['symmetric_key']}...")
    encrypted_sym_key = public_key.encrypt(sym_key, get_asym_padding())

    with open(settings['symmetric_key'], 'wb') as sym_out:
        sym_out.write(encrypted_sym_key)

    print("--Key generation has been completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="RSA & SEED hybrid encryption")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Key generation mode')
    group.add_argument('-enc', '--encryption', action='store_true', help='Encryption mode')
    group.add_argument('-dec', '--decryption', action='store_true', help='Decryption mode')

    parser.add_argument('-c', '--config', default='settings.json',
                        help='Path to the configuration file (settings.json by defaul)')

    args = parser.parse_args()
    
    try:
        settings = load_settings(args.config)

        if args.generation:
            generate_keys(settings)
        elif args.encryption:
            encrypt_data(settings)
        elif args.decryption:
            decrypt_data(settings)




if __name__ == '__main__':
    main()