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


def encrypt_data(settings: dict):
    """Data encryption by a hybrid system."""
    print("\n!!STARTING DATA ENCRYPTION!!")

    print("-Uploading the RSA private key...")
    with open(settings['secret_key'], 'rb') as pem_in:
        private_key = serialization.load_pem_private_key(pem_in.read(), password=None)

    print("-Reading and decrypting the symmetric SEED key...")
    with open(settings['symmetric_key'], 'rb') as sym_in:
        encrypted_sym_key = sym_in.read()

    sym_key = private_key.decrypt(encrypted_sym_key, get_asym_padding())

    print(f"-Reading the source file {settings['initial_file']}...")
    with open(settings['initial_file'], 'rb') as f_in:
        plain_text = f_in.read()

    padder = sym_padding.ANSIX923(128).padder()
    padded_text = padder.update(plain_text) + padder.finalize()

    print("-Data encryption using the SEED algorithm...")
    iv = os.urandom(16)
    cipher = Cipher(algorithms.SEED(sym_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_text) + encryptor.finalize()

    print(f"-Saving an encrypted file in {settings['encrypted_file']}...")
    with open(settings['encrypted_file'], 'wb') as f_out:
        f_out.write(iv + cipher_text)

    print("--The encryption has been successfully completed!")

def main():
    parser = argparse.ArgumentParser(description="RSA & SEED hybrid encryption")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Key generation mode')
    group.add_argument('-enc', '--encryption', action='store_true', help='Encryption mode')
    group.add_argument('-dec', '--decryption', action='store_true', help='Decryption mode')

    parser.add_argument('-c', '--config', default='settings.json',
                        help='Path to the configuration file (settings.json by default)')

    args = parser.parse_args()
    
    try:
        settings = load_settings(args.config)

        if args.generation:
            generate_keys(settings)
        elif args.encryption:
            encrypt_data(settings)
        elif args.decryption:
            decrypt_data(settings)
    except FileNotFoundError as e:
        print(f"!!!Error: File not found: {e.filename}")
    except ValueError as e:
        print(f"!!!Error: File damaged: {e}")
    except Exception as e:
        print(f"!!!Error: Unexpected error: {e}")


if __name__ == '__main__':
    main()