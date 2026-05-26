import json
from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes

def load_settings(filepath: str = 'settings.json') -> Dict[str, Any]:
    """Загружает конфигурационные настройки из JSON файла.

    Args:
        filepath (str): Путь к файлу конфигурации. По умолчанию 'settings.json'.

    Returns:
        Dict[str, Any]: Словарь со структурированными путями и параметрами лабы.
    """
    try:
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"[-] Файл {filepath} не найден!")
        exit(1)

def get_asym_padding() -> asym_padding.OAEP:
    """Возвращает настроенную схему паддинга RSA-OAEP.

    Использует алгоритм хэширования SHA-256 для MGF1 и главного хэша.

    Returns:
        asym_padding.OAEP: Объект асимметричного паддинга для RSA.
    """
    return asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )