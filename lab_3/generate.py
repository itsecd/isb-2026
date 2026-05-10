from asymmetric import encrypt_symmetric_key, generate_rsa_keys
from symmetric import generate_symmetric_key
from utils import save_private_key, save_public_key, write_bytes


def generate_key(
    path_symmetric_key: str,
    path_asymmetric_public_key: str,
    path_asymmetric_private_key: str,
) -> None:
    """
    Генерирует симметричный ключ SEED и пару RSA ключей.
    Симметричный ключ шифруется открытым RSA ключом.

    Args:
        path_symmetric_key: путь для сохранения зашифрованного симметричного ключа
        path_asymmetric_public_key: путь для сохранения открытого RSA ключа
        path_asymmetric_private_key: путь для сохранения закрытого RSA ключа
    """
    print("Генерация симметричного ключа:")
    try:
        symmetric_key = generate_symmetric_key()
    except Exception as e:
        raise RuntimeError(f"Симметричный ключ не сгенерировался: {e}")
    print("Симметричный ключ сгенерирован")

    print("Генерация RSA ключей (открытый и закрытый):")
    try:
        private_key, public_key = generate_rsa_keys()
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
    encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, public_key)
    print("Симметричный ключ зашифрован")

    print(f"Сохранение симметричного ключа в {path_symmetric_key}:")
    write_bytes(path_symmetric_key, encrypted_symmetric_key)
    print("Генерация завершена успешно")