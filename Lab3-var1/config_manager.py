import json
import os

DEFAULT_SETTINGS = {
    "public_key_path": "keys/public.pem",
    "private_key_path": "keys/private.pem",
    "enc_symmetric_key_path": "keys/aes_key.enc",
    "default_aes_key_size": 256,
    "default_input_file": "data/plaintext.txt",
    "default_encrypted_file": "data/encrypted.bin",
    "default_decrypted_file": "data/decrypted.txt"
}

def save_settings(settings, path="settings.json"):
    with open(path, 'w') as f:
        json.dump(settings, f, indent=2)

def load_settings(path="settings.json"):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        return DEFAULT_SETTINGS.copy()
