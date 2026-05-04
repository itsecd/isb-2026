from .symmetric import generate_camellia_key
from .asymmetric import generate_rsa_keypair, save_public_key, save_private_key, encrypt_with_rsa
from .utils import write_binary_file


def run_key_generation(public_key_path: str, private_key_path: str, 
                       symmetric_key_path: str, encrypted_symmetric_key_path: str) -> None:
    """
    Запуск режима генерации ключей
    
     - Генерация симметричного ключа (Camellia)
     - Генерация асимметричных ключей (RSA)
     - Сохранение ключей
     - Зашифрование симметричного ключа открытым ключом
    """
    print("\n" + "="*60)
    print("Режим 1: Генерация ключей системы")
    print("="*60)
    
    print("\n Генерация симметричного ключа...")
    symmetric_key = generate_camellia_key(32)
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