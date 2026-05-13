from .symmetric import generate_camellia_key
from .asymmetric import generate_rsa_keypair, save_public_key, save_private_key, encrypt_with_rsa
from .utils import write_binary_file


def run_key_generation(public_key_path: str, private_key_path: str, 
                       symmetric_key_path: str, encrypted_symmetric_key_path: str) -> None:
    """
    Запуск режима генерации ключей.
    
    Выполняет полную генерацию всех ключей для гибридной криптосистемы:
    1. Генерирует симметричный ключ Camellia (256 бит)
    2. Генерирует асимметричную пару RSA ключей (2048 бит)
    3. Сохраняет все ключи в указанные файлы
    4. Зашифровывает симметричный ключ публичным RSA ключом
    
    Процесс генерации:
        - Симметричный ключ -> сохраняется в файл
        - RSA ключи (публичный + приватный) -> сохраняются в файлы
        - Симметричный ключ шифруется публичным RSA ключом -> сохраняется
    
    Args:
        public_key_path (str): Путь для сохранения публичного RSA ключа
        private_key_path (str): Путь для сохранения приватного RSA ключа
        symmetric_key_path (str): Путь для сохранения симметричного ключа Camellia
        encrypted_symmetric_key_path (str): Путь для сохранения зашифрованного симметричного ключа
    
    Returns:
        None
    
    Raises:
        IOError: Если нет прав на запись в файлы
        ValueError: При ошибках генерации ключей
    
    Example:
        >>> run_key_generation(
        ...     public_key_path='keys/public.pem',
        ...     private_key_path='keys/private.pem',
        ...     symmetric_key_path='keys/symmetric.key',
        ...     encrypted_symmetric_key_path='keys/encrypted_symmetric.key'
        ... )
    """
    print("\n" + "="*60)
    print("Режим 1: Генерация ключей системы")
    print("="*60)
    
    print("\n Генерация симметричного ключа...")
    symmetric_key = generate_camellia_key(32)  # 32 байта = 256 бит
    write_binary_file(symmetric_key_path, symmetric_key)
    print(f" Симметричный ключ сохранен: {symmetric_key_path}")
    
    print("\n Генерация асимметричных ключей...")
    private_key, public_key = generate_rsa_keypair()

    print("\n Сохранение ключей...")
    save_public_key(public_key, public_key_path)
    save_private_key(private_key, private_key_path)

    print("\n Зашифрование симметричного ключа открытым ключом...")
    encrypted_key = encrypt_with_rsa(symmetric_key, public_key_path)
    write_binary_file(encrypted_symmetric_key_path, encrypted_key)
    print(f" Зашифрованный симметричный ключ сохранен: {encrypted_symmetric_key_path}")
    
    print("\n" + "="*60)
    print(" Генерация ключей завершена!")
    print("="*60)