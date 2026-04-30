from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .utils import unpad_data
from .key_generator import load_private_key


def decrypt_symmetric_key_with_rsa(encrypted_key_path: str, private_key_path: str) -> bytes:
    """Расшифровка симметричного ключа приватным RSA ключом"""
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
    
    print(" Загрузка приватного RSA ключа...")
    private_key = load_private_key(private_key_path)
    
    with open(encrypted_key_path, 'rb') as f:
        encrypted_key = f.read()
    
    print(" Расшифровка симметричного ключа...")
    symmetric_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return symmetric_key


def decrypt_data_with_camellia(encrypted_data_with_iv: bytes, key: bytes) -> bytes:
    """
    Расшифровка данных алгоритмом Camellia 

    """
    iv = encrypted_data_with_iv[:16]
    encrypted_data = encrypted_data_with_iv[16:]
    
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    
    return unpad_data(decrypted_padded, block_size=16)


def run_decryption(encrypted_file: str, private_key_path: str, 
                   encrypted_symmetric_key_path: str, output_file: str) -> None:
    """
    Запуск режима дешифрования 
    
    Входные параметры:
        1) путь к зашифрованному текстовому файлу
        2) путь к закрытому ключу ассиметричного алгоритма
        3) путь к зашифрованному ключу симметричного алгоритма
        4) путь, по которому сохранить расшифрованный текстовый файл
    """
    print("\n" + "="*60)
    print("Режим 3: Дешифрование данных гибридной системой")
    print("="*60)
    
    print("\n Расшифровка симметричного ключа")
    symmetric_key = decrypt_symmetric_key_with_rsa(encrypted_symmetric_key_path, private_key_path)
    print(f" Симметричный ключ получен (длина: {len(symmetric_key)} байт)")
    
    print(f"\n Чтение зашифрованного файла: {encrypted_file}")
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()
    print(f" Размер {len(encrypted_data)} байт")
    
    print("\n Расшифровка данных алгоритмом Camellia")
    decrypted_data = decrypt_data_with_camellia(encrypted_data, symmetric_key)
    
    print(f"\n Сохранение расшифрованного файла: {output_file}")
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
    
    print("\n" + "="*60)
    print(" Дешифрование завершено!")
    print(f" Зашифрованный файл: {encrypted_file}")
    print(f" Расшифрованный файл: {output_file}")
    print("="*60)
    
    try:
        preview = decrypted_data[:200].decode('utf-8')
        print(f"\nПревью расшифрованного текста:")
        print("-" * 50)
        print(preview + ("..." if len(decrypted_data) > 200 else ""))
        print("-" * 50)
    except UnicodeDecodeError:
        pass