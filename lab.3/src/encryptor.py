from .utils import read_text_file, write_binary_file
from .asymmetric import decrypt_with_rsa
from .symmetric import encrypt_with_camellia


def run_encryption(input_file: str, private_key_path: str, 
                   encrypted_symmetric_key_path: str, output_file: str) -> None:
    """
    Режим шифрования
    
     - Расшифровка симметричного ключа (RSA)
     - Шифрование текста (Camellia)
    """
    print("\n" + "="*60)
    print("Режим 2: Шифрование данных сиситемой")
    print("="*60)
    
    # 2.1
    print("\n Расшифровка симметричного ключа...")
    with open(encrypted_symmetric_key_path, 'rb') as f:
        encrypted_key = f.read()
    symmetric_key = decrypt_with_rsa(encrypted_key, private_key_path)
    print(f" Симметричный ключ получен ({len(symmetric_key)} байт)")
    
    # 2.2
    print(f"\n Чтение исходного файла: {input_file}")
    plaintext = read_text_file(input_file)
    print(f" Прочитано {len(plaintext)} байт")
    
    print(" Шифрование данных Camellia...")
    encrypted_data = encrypt_with_camellia(plaintext, symmetric_key)
    
    print(f" Сохранение зашифрованного файла: {output_file}")
    write_binary_file(output_file, encrypted_data)
    
    print("\n" + "="*60)
    print(" Шифрование завершено!")
    print(f" Исходный файл: {input_file}")
    print(f" Зашифрованный файл: {output_file}")
    print("="*60)