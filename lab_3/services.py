import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import crypto

def load_private_key(private_pem_path: str):
    """
    Вспомогательная функция для чтения закрытого ключа из файла.
    """
    with open(private_pem_path, 'rb') as pem_in:
        private_bytes = pem_in.read()
        return load_pem_private_key(private_bytes, password=None)

def generate_keys(path_to_cyph: str, path_to_public_key: str, path_to_private_key: str):
    """
        Генерирует и сохраняет ключи в новом файле:

        :path_to_cyph: Путь для сохранения зашифрованного ключа IDEA.
        :path_to_pub: Путь для сохранения открытого ключа RSA.
        :path_to_priv: Путь для сохранения закрытого ключа RSA.
    """
    idea_key = crypto.generate_idea_key()
    print(f"Сгенерирован новый IDEA ключ: {idea_key}")

    private_key, public_key = crypto.generate_rsa_keypair()
    print("Сгенерирован public key\nСгенерирован private key")

    public_pem = os.path.join(path_to_public_key, 'public.pem')
    with open(public_pem, 'wb') as public_out:
        public_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    with open(path_to_private_key, 'wb') as private_out:
        private_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    encrypted_idea_key = crypto.encrypt_idea_key_rsa(idea_key, public_key)
    print(f"Зашифрованный IDEA ключ (в байтах): {encrypted_idea_key.hex()}")

    filename = os.path.join(path_to_cyph, 'symmetric_encrypted.bin')
    with open(filename, 'wb') as key_file:
        key_file.write(encrypted_idea_key)

    print("Ключи серилизованы и записаны в файлы!")

def encrypt_message(path_to_message: str, private_pem: str, path_to_cyph_key: str, path_to_save: str):
    """
        Зашифровывает и сохраняет в файл сообщение

        :path_to_cyph: Путь для сохранения зашифрованного ключа IDEA.
        :path_to_message: Путь до сообщения, которое требуется зашифровать
        :path_to_save: Путь куда следует сохранить
    """
    with open(path_to_message, 'rb') as message_file:
        text = message_file.read()

    with open(path_to_cyph_key, 'rb') as c_file:
        c_text = c_file.read()

    d_private_key = load_private_key(private_pem)
    dc_key = crypto.decrypt_idea_key_rsa(c_text, d_private_key)

    iv, cyph_text = crypto.encrypt_data_idea(text, dc_key)

    filename = os.path.join(path_to_save, "encrypted.txt")
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(iv + cyph_text)

    print(f"Зашифрованный текст сохранен в файл: {filename}")

def decrypt_text(path_to_message: str, private_pem: str, path_to_cyph_key: str, path_to_save: str):
    """
        Расшифровывает и сохраняет сообщение

        :path_to_cyph: Путь для сохранения зашифрованного ключа IDEA.
        :path_to_message: Путь до сообщения, которое требуется зашифровать
        :path_to_save: Путь куда следует сохранить
        :private_pem: Путь до закрытого ключа
    """
    with open(path_to_message, 'rb') as f:
        combined_data = f.read()

    with open(path_to_cyph_key, 'rb') as c_file:
        c_text = c_file.read()

    d_private_key = load_private_key(private_pem)
    
    iv = combined_data[:8]
    actual_cyph_text = combined_data[8:]

    dc_key = crypto.decrypt_idea_key_rsa(c_text, d_private_key)

    unpadded_dc_text = crypto.decrypt_data_idea(actual_cyph_text, iv, dc_key)

    print(unpadded_dc_text.decode('UTF-8'))

    filename = os.path.join(path_to_save, 'decrypted.txt')
    with open(filename, 'wb') as decrypted_text:
        decrypted_text.write(unpadded_dc_text)