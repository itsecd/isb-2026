from .utils import read_binary_file, write_text_file
from .asymmetric import decrypt_with_rsa
from .symmetric import decrypt_with_camellia


def run_decryption(encrypted_file: str, private_key_path: str, 
                   encrypted_symmetric_key_path: str, output_file: str) -> None:
    """
    Режим дешифрования данных.
    
    Выполняет полный цикл дешифрования гибридной криптосистемы:
    1. Расшифровывает симметричный ключ с помощью RSA приватного ключа
    2. Расшифровывает данные с помощью Camellia, используя полученный ключ
    3. Сохраняет расшифрованные данные в выходной файл
    
    Процесс дешифрования:
        Зашифрованные данные (RSA) -> Симметричный ключ -> Расшифровка Camellia -> Исходные данные
    
    Формат входных данных:
        - Зашифрованный симметричный ключ: RSA-зашифрованные данные
        - Зашифрованный файл: [IV (16 байт)] + [Camellia-зашифрованные данные]
    
    Args:
        encrypted_file (str): Путь к зашифрованному файлу (выход encryptor'а)
        private_key_path (str): Путь к приватному RSA ключу для расшифровки симметричного ключа
        encrypted_symmetric_key_path (str): Путь к файлу с зашифрованным симметричным ключом
        output_file (str): Путь для сохранения расшифрованных данных
    
    Returns:
        None
    
    Raises:
        FileNotFoundError: Если любой из входных файлов не существует
        ValueError: Если ключ имеет неверный размер или данные повреждены
        Exception: При ошибках расшифровки (неверный ключ, повреждённые данные)
    
    Example:
        >>> run_decryption(
        ...     encrypted_file='data/encrypted.bin',
        ...     private_key_path='keys/private.pem',
        ...     encrypted_symmetric_key_path='keys/encrypted_symmetric.key',
        ...     output_file='data/decrypted.txt'
        ... )
        
    Notes:
        Функция выводит информационные сообщения о ходе выполнения:
        - Статус расшифровки симметричного ключа
        - Размер прочитанных данных
        - Результат сохранения файла
        - Превью расшифрованного текста (если это текст в кодировке UTF-8)
    """
    print("\n" + "="*60)
    print("Режим 3: Дешифрование данных системой")
    print("="*60)
    
    print("\n Расшифровка симметричного ключа...")
    encrypted_key = read_binary_file(encrypted_symmetric_key_path)
    symmetric_key = decrypt_with_rsa(encrypted_key, private_key_path)
    print(f" Симметричный ключ получен ({len(symmetric_key)} байт)")
    
    print(f"\n Чтение зашифрованного файла: {encrypted_file}")
    encrypted_data = read_binary_file(encrypted_file)
    print(f" Прочитано {len(encrypted_data)} байт")
    
    print(" Расшифровка данных Camellia...")
    decrypted_data = decrypt_with_camellia(encrypted_data, symmetric_key)
    
    print(f" Сохранение расшифрованного файла: {output_file}")
    write_text_file(output_file, decrypted_data)
    
    print("\n" + "="*60)
    print(" Дешифрование завершено!")
    print(f"  - Зашифрованный файл: {encrypted_file}")
    print(f"  - Расшифрованный файл: {output_file}")
    print("="*60)
    
    try:
        preview = decrypted_data[:200].decode('utf-8')
        print(f"\n[Расшифрованный текст]:")
        print("-" * 50)
        print(preview + ("..." if len(decrypted_data) > 200 else ""))
        print("-" * 50)
    except UnicodeDecodeError:
        print("\n[Расшифрованные данные являются бинарными]")