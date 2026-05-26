from typing import Dict, Any
from cryptography.hazmat.primitives import serialization, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from utils import get_asym_padding

def decrypt_data(settings: Dict[str, Any]) -> None:
    """Выполняет дешифрование ранее зашифрованного файла.

    Восстанавливает ключ Camellia через закрытый ключ RSA, считывает IV 
    из первых 16 байт зашифрованного файла, расшифровывает основной шифротекст 
    в режиме CBC и производит депаддинг ANSIX923.

    Args:
        settings (Dict[str, Any]): Конфигурационный словарь с путями к файлам.
    """
    print("Запуск режима дешифрования...")
    
    try:
        with open(settings['secret_key'], 'rb') as pem_in:
            private_bytes = pem_in.read()
        private_key = serialization.load_pem_private_key(private_bytes, password=None)
    except FileNotFoundError:
        print(f"Файл {settings['secret_key']} не найден!")
        return
    
    try:
        with open(settings['symmetric_key'], 'rb') as sym_in:
            enc_sym_key = sym_in.read()
        
        sym_key = private_key.decrypt(enc_sym_key, get_asym_padding())
        print("Симметричный ключ успешно расшифрован.")
    except FileNotFoundError:
        print(f"Файл {settings['symmetric_key']} не найден!")
        return

    try:
        with open(settings['encrypted_file'], 'rb') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Файл {settings['encrypted_file']} не найден!")
        return

    iv = file_content[:16]
    c_text = file_content[16:]
    
    cipher = Cipher(algorithms.Camellia(sym_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_dc_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = sym_padding.ANSIX923(128).unpadder()
    dc_text = unpadder.update(padded_dc_text) + unpadder.finalize()

    try:
        with open(settings['decrypted_file'], 'wb') as f:
            f.write(dc_text)
        print(f"Данные успешно дешифрованы и сохранены в: {settings['decrypted_file']}.")
        print("Дешифрование завершено!\n")
    except IOError as e:
        print(f"Ошибка при сохранении дешифрованного файла: {e}")
        return