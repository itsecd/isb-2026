import os
import json
from symmetric import unpack_encrypted_data, pack_encrypted_data

def read_file(filepath: str) -> bytes:
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e


def write_text(filepath, text):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        raise RuntimeError(f"Couldn't write in file: {filepath}") from e


def load_settings(filepath: str):
    try:
        with open(filepath) as json_file:
            return json.load(json_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e 
    

def load_encrypted_file(filepath: str) -> tuple[bytes, bytes]:
    try:
        with open(filepath, 'rb') as enc_file:
            data = enc_file.read()
        return unpack_encrypted_data(data)
    
    except Exception as e:
        raise RuntimeError(f"Couldn't load encrypted text {filepath}") from e
    


def write_encrypted_file(filepath: str, nonce: bytes, ciphertext: bytes) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    packed = pack_encrypted_data(nonce, ciphertext)
    
    with open(filepath, 'wb') as f:
        f.write(packed)