from .utils import read_text_file, write_binary_file, read_binary_file
from .asymmetric import decrypt_with_rsa
from .symmetric import encrypt_with_camellia


def run_encryption(input_file: str, private_key_path: str, 
                   encrypted_symmetric_key_path: str, output_file: str) -> None:
    """
    Режим шифрования данных.
    
    Выполняет шифрование данных с использованием гибридной криптосистемы:
    1. Расшифровывает симметричный ключ с помощью RSA приватного ключа
    2. Шифрует входные данные алгоритмом Camellia
    3. Сохраняет зашифрованные данные в выходной файл
    
    Args:
        input_file (str): Путь к исходному файлу для шифрования
        private_key_path (str): Путь к приватному RSA ключу для расшифровки симметричного ключа
        encrypted_symmetric_key_path (str): Путь к зашифрованному симметричному ключу
        output_file (str): Путь для сохранения зашифрованных данных
    
    Returns:
        None
    
    Raises:
        FileNotFoundError: Если входной файл или файл с зашифрованным ключом не существует
        ValueError: Если ключ имеет неверный размер
        Exception: При ошибках шифрования
    """
    print("\n" + "="*60)
    print("Режим 2: Шифрование данных системой")
    print("="*60)
    
    print("\n Расшифровка симметричного ключа...")
    encrypted_key = read_binary_file(encrypted_symmetric_key_path)
    symmetric_key = decrypt_with_rsa(encrypted_key, private_key_path)
    print(f" Симметричный ключ получен ({len(symmetric_key)} байт)")
    
    print(f"\n Чтение исходного файла: {input_file}")
    plaintext = read_text_file(input_file)
    print(f" Прочитано {len(plaintext)} байт")
    
    print(" Шифрование данных Camellia...")
    encrypted_data = encrypt_with_camellia(plaintext, symmetric_key)
    
    print(f" Сохранение зашифрованного файла: {output_file}")
    write_binary_file(output_file, encrypted_data)
    
    print("\n" + "="*60)
    print(" Шифрование завершено!")
    print(f"  - Исходный файл: {input_file}")
    print(f"  - Зашифрованный файл: {output_file}")
    print("="*60)