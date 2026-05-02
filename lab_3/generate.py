import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa

from utils import save_private_key, save_public_key, write_bytes


def generate_key(
    path_symmetric_key: str,
    path_asymmetric_public_key: str,
    path_asymmetric_private_key: str,
) -> None:
    """
    Функция для генерируации симметричного ключа SEED и пары RSA ключей.
    Симметричный ключ шифруется открытым RSA ключом и сохраняется на диск.
    Открытый и закрытый RSA ключи сохраняются в PEM формате.
    """
    print("Генерация симметричного ключа:")
    try:
        symmetric_key = os.urandom(16)
    except Exception as e:
        raise RuntimeError(f"Симметричный ключ не сгенерировался: {e}")
    print("Симметричный ключ сгенерирован")

    print("Генерация RSA ключей (открытый и закрытый):")
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
    except Exception as e:
        raise RuntimeError(f"RSA ключи не сгенерировались: {e}")
    print("RSA ключи сгенерированы")

    print(f"Сохранение открытого ключа в {path_asymmetric_public_key}:")
    save_public_key(path_asymmetric_public_key, public_key)
    print("Открытый ключ сохранён")

    print(f"Сохранение закрытого ключа в {path_asymmetric_private_key}:")
    save_private_key(path_asymmetric_private_key, private_key)
    print("Закрытый ключ сохранён")

    print("Шифрование симметричного ключа открытым RSA ключом:")
    try:
        symmetric_key = public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise RuntimeError(f"Симметричный ключ не зашифровался: {e}")
    print("Симметричный ключ зашифрован")

    print(f"Сохранение симметричного ключа в {path_symmetric_key}:")
    write_bytes(path_symmetric_key, symmetric_key)
    print("Генерация завершена успешно")