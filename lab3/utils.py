import json
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes

def load_settings(filepath='settings.json'):
    """Загрузка конфигурации из JSON файла."""
    try:
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"[-] Файл {filepath} не найден!")
        exit(1)

def get_asym_padding():
    """Возвращает схему паддинга для RSA (RSA-OAEP)."""
    return asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )