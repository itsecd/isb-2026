"""
Модуль реализации режимов работы гибридной криптосистемы.

Предоставляет три основных режима:
1. Генерация ключей (симметричных и асимметричных)
2. Шифрование файлов
3. Расшифровка файлов
"""

from . import io_utils
from . import symmetrical
from . import asymmetrical


def generate_keys_mode(config: dict) -> None:
    """
    Генерирует все необходимые ключи для гибридной криптосистемы.
    
    Args:
        config: Словарь с конфигурацией, содержащий пути и параметры.
        
    Process:
        1. Генерирует симметричный ключ SM4 (128 бит)
        2. Генерирует пару ключей RSA (2048 бит)
        3. Сериализует RSA ключи в PEM формат
        4. Шифрует симметричный ключ публичным RSA ключом
        5. Сохраняет все ключи по указанным путям
    """
    print("Генерация симметричного ключа SM4...")
    symmetric_key = symmetrical.generate_symmetric_key(config['sm4_key_size'])
    io_utils.write_binary_file(config['symmetric_key'], symmetric_key)
    
    print("Генерация пары ключей RSA...")
    private_key, public_key = asymmetrical.generate_rsa_keypair(
        key_size=config['rsa_key_size'],
        public_exponent=config['rsa_public_exponent']
    )
    
    print("Сериализация асимметричных ключей...")
    private_pem = asymmetrical.serialize_private_key(private_key)
    public_pem = asymmetrical.serialize_public_key(public_key)
    
    io_utils.write_binary_file(config['private_key'], private_pem)
    io_utils.write_binary_file(config['public_key'], public_pem)
    
    print("Шифрование симметричного ключа...")
    encrypted_symmetric_key = asymmetrical.encrypt_symmetric_key(
        public_key,
        symmetric_key
    )
    io_utils.write_binary_file(config['encrypted_symmetric_key'], encrypted_symmetric_key)
    
    print("Ключи успешно сгенерированы и сохранены.")


def encrypt_mode(config: dict) -> None:
    """
    Шифрует файл с использованием гибридной криптосистемы.
    
    Args:
        config: Словарь с конфигурацией, содержащий пути и параметры.
        
    Process:
        2.1. Расшифровывает симметричный ключ приватным RSA ключом
        2.2. Шифрует файл симметричным алгоритмом SM4
    """
    print("Расшифровка симметричного ключа...")
    private_key = asymmetrical.load_private_key(config['private_key'])
    encrypted_symmetric_key = io_utils.read_binary_file(config['encrypted_symmetric_key'])
    symmetric_key = asymmetrical.decrypt_symmetric_key(
        private_key,
        encrypted_symmetric_key
    )
    
    print("Шифрование файла алгоритмом SM4...")
    symmetrical.encrypt_file_sm4(
        config['initial_file'],
        config['encrypted_file'],
        symmetric_key,
        config['block_size']
    )
    
    print("[✓] Файл успешно зашифрован.")


def decrypt_mode(config: dict) -> None:
    """
    Расшифровывает файл с использованием гибридной криптосистемы.
    
    Args:
        config: Словарь с конфигурацией, содержащий пути и параметры.
        
    Process:
        3.1. Расшифровывает симметричный ключ приватным RSA ключом
        3.2. Расшифровывает файл симметричным алгоритмом SM4
    """
    print("Расшифровка симметричного ключа...")
    private_key = asymmetrical.load_private_key(config['private_key'])
    encrypted_symmetric_key = io_utils.read_binary_file(config['encrypted_symmetric_key'])
    symmetric_key = asymmetrical.decrypt_symmetric_key(
        private_key,
        encrypted_symmetric_key
    )
    
    print("Расшифровка файла алгоритмом SM4...")
    symmetrical.decrypt_file_sm4(
        config['encrypted_file'],
        config['decrypted_file'],
        symmetric_key,
        config['block_size']
    )
    
    print("Файл успешно расшифрован.")