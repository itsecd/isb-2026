import os 
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def load_config(path='settings.json') -> dict:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: settings.json not found")
        return {}


def triple_des_key_generation(key_size: int, config: dict):
    triple_des_key = os.urandom(key_size) 

    file_name = config.get('symmetric_key', 'session_key/session_key.pem') 
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, 'wb') as key_file:
        key_file.write(triple_des_key)   
    print("session key is generated and saved")


def rsa_key_generation(config: dict, username: str):
    user_config = config["users"].get(username)
    if not user_config:
        raise ValueError(f"User {username} not found in config")

    private_key_path = user_config["private_key"]
    public_key_path = user_config["public_key"]

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    with open(private_key_path, 'wb') as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    print(f"Private key for {username} saved")

    with open(public_key_path, 'wb') as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    print(f"Public key for {username} saved")


def load_public_key(path: str):
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read())
    
def encrypt_session_key(session_key: bytes, public_key):
    encrypted_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

def save_encrypted_key(path: str, encrypted_key: bytes):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb') as f:
        f.write(encrypted_key)

def encrypt_session_key_for_user(config: dict, username: str):
    public_key_path = config['users'][username]['public_key']
    session_key_path = config.get('symmetric_key')

    with open(session_key_path, 'rb') as f:
        session_key = f.read()

    public_key = load_public_key(public_key_path)
    encrypted_key = encrypt_session_key(session_key, public_key)

    save_path = f"encrypted_keys/{username}_session_key.enc"
    save_encrypted_key(save_path, encrypted_key)
    print(f"Session key encrypted for {username}")




    


value: int =0 #64, 128, 192 бит, т.е. значение в бтиах делим на 8. Задать пользовательский ввод