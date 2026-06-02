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


def generate_keys_mode(
    symmetric_key_path: str,
    encrypted_symmetric_key_path: str,
    public_key_path: str,
    private_key_path: str
) -> None:
    """
    Генерирует все необходимые ключи для гибридной криптосистемы.
    
    Args:
        symmetric_key_path: Путь для сохранения симметричного ключа.
        encrypted_symmetric_key_path: Путь для сохранения зашифрованного симметричного ключа.
        public_key_path: Путь для сохранения публичного RSA ключа.
        private_key_path: Путь для сохранения приватного RSA ключа.
        
    Process:
        1. Генерирует симметричный ключ SM4 (128 бит)
        2. Генерирует пару ключей RSA (2048 бит)
        3. Сериализует RSA ключи в PEM формат
        4. Шифрует симметричный ключ публичным RSA ключом
        5. Сохраняет все ключи по указанным путям
    """
    print("Генерация симметричного ключа SM4")
    symmetric_key = symmetrical.generate_symmetric_key()
    io_utils.write_binary_file(symmetric_key_path, symmetric_key)
    
    print("Генерация пары ключей RSA")
    private_key, public_key = asymmetrical.generate_rsa_keypair()
    
    print("Сериализация асимметричных ключей")
    private_pem = asymmetrical.serialize_private_key(private_key)
    public_pem = asymmetrical.serialize_public_key(public_key)
    
    io_utils.write_binary_file(private_key_path, private_pem)
    io_utils.write_binary_file(public_key_path, public_pem)
    
    print("Шифрование симметричного ключа")
    encrypted_symmetric_key = asymmetrical.encrypt_symmetric_key(
        public_key, 
        symmetric_key
    )
    io_utils.write_binary_file(encrypted_symmetric_key_path, encrypted_symmetric_key)
    
    print("Ключи успешно сгенерированы и сохранены.")


def encrypt_mode(
    input_path: str,
    output_path: str,
    private_key_path: str,
    encrypted_symmetric_key_path: str
) -> None:
    """
    Шифрует файл с использованием гибридной криптосистемы.
    
    Args:
        input_path: Путь к исходному файлу.
        output_path: Путь для сохранения зашифрованного файла.
        private_key_path: Путь к приватному RSA ключу.
        encrypted_symmetric_key_path: Путь к зашифрованному симметричному ключу.
        
    Process:
        2.1. Расшифровывает симметричный ключ приватным RSA ключом
        2.2. Шифрует файл симметричным алгоритмом SM4
    """
    print("Расшифровка симметричного ключа...")
    private_key = asymmetrical.load_private_key(private_key_path)
    encrypted_symmetric_key = io_utils.read_binary_file(encrypted_symmetric_key_path)
    symmetric_key = asymmetrical.decrypt_symmetric_key(
        private_key,
        encrypted_symmetric_key
    )
    
    print("Шифрование файла алгоритмом SM4")
    symmetrical.encrypt_file_sm4(input_path, output_path, symmetric_key)
    
    print("Файл успешно зашифрован.")


def decrypt_mode(
    input_path: str,
    output_path: str,
    private_key_path: str,
    encrypted_symmetric_key_path: str
) -> None:
    """
    Расшифровывает файл с использованием гибридной криптосистемы.
    
    Args:
        input_path: Путь к зашифрованному файлу.
        output_path: Путь для сохранения расшифрованного файла.
        private_key_path: Путь к приватному RSA ключу.
        encrypted_symmetric_key_path: Путь к зашифрованному симметричному ключу.
        
    Process:
        3.1. Расшифровывает симметричный ключ приватным RSA ключом
        3.2. Расшифровывает файл симметричным алгоритмом SM4
    """
    print("Расшифровка симметричного ключа")
    private_key = asymmetrical.load_private_key(private_key_path)
    encrypted_symmetric_key = io_utils.read_binary_file(encrypted_symmetric_key_path)
    symmetric_key = asymmetrical.decrypt_symmetric_key(
        private_key,
        encrypted_symmetric_key
    )
    
    print("Расшифровка файла алгоритмом SM4")
    symmetrical.decrypt_file_sm4(input_path, output_path, symmetric_key)
    
    print("Файл успешно расшифрован.")