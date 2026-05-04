from .utils import read_binary_file, write_text_file
from .asymmetric import decrypt_with_rsa
from .symmetric import decrypt_with_camellia


def run_decryption(encrypted_file: str, private_key_path: str, 
                   encrypted_symmetric_key_path: str, output_file: str) -> None:
    """
    Режим дешифрования
    
    - Расшифровка симметричного ключа (RSA)
    - Расшифровка текста (Camellia)
    """
    print("\n" + "="*60)
    print("Режим 3: Дешифрование данных системой")
    print("="*60)
    
    # 3.1
    print("\n Расшифровка симметричного ключа...")
    encrypted_key = read_binary_file(encrypted_symmetric_key_path)
    symmetric_key = decrypt_with_rsa(encrypted_key, private_key_path)
    print(f" Симметричный ключ получен ({len(symmetric_key)} байт)")
    
    # 3.2
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
    
    # Превью
    try:
        preview = decrypted_data[:200].decode('utf-8')
        print(f"\n[Расшифрованный текст]:")
        print("-" * 50)
        print(preview + ("..." if len(decrypted_data) > 200 else ""))
        print("-" * 50)
    except UnicodeDecodeError:
        pass