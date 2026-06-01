from asymmetric import RSAKeyManager
from symmetric import BlowfishCipher
from utils import read_bytes, write_bytes


class HybridCrypto:
    
    def __init__(self):
        self.rsa = RSAKeyManager()
        self.blowfish = BlowfishCipher()
    
    def generate_keys(self, public_path, private_path, encrypted_key_path, key_length):
        """
        Генерирует полный набор ключей для гибридной криптосистемы.
        
        Args:
            public_path: Путь для сохранения публичного RSA ключа
            private_path: Путь для сохранения приватного RSA ключа
            encrypted_key_path: Путь для сохранения зашифрованного ключа Blowfish
            key_length: Длина ключа Blowfish в битах
        """
        sym_key = self.blowfish.generate_key(key_length)
        priv, pub = self.rsa.generate_pair()
        self.rsa.save_private(private_path, priv)
        self.rsa.save_public(public_path, pub)
        encrypted_sym = self.rsa.encrypt(pub, sym_key)
        write_bytes(encrypted_key_path, encrypted_sym)
        print(f"Ключи сохранены (Blowfish: {key_length} бит)")
    
    def encrypt_file(self, input_path, output_path, public_key_path, encrypted_key_path, key_length=128):
        """
        Выполняет гибридное шифрование файла.
    
        Args:
            input_path: Путь к исходному файлу
            output_path: Путь для сохранения зашифрованного файла
            public_key_path: Путь к ПУБЛИЧНОМУ RSA ключу
            encrypted_key_path: Путь к зашифрованному ключу Blowfish
            key_length: Длина ключа Blowfish
        """
        pub = self.rsa.load_public(public_key_path)
        sym_key = self.blowfish.generate_key(key_length)
        encrypted_sym = self.rsa.encrypt(pub, sym_key)
        write_bytes(encrypted_key_path, encrypted_sym)
        data = read_bytes(input_path)
        encrypted_data = self.blowfish.encrypt(sym_key, data)
        write_bytes(output_path, encrypted_data)
        print(f"Файл зашифрован: {output_path}")
    
    def decrypt_file(self, input_path, output_path, private_key_path, encrypted_key_path):
        """
        Выполняет гибридное дешифрование файла.
        
        Args:
            input_path: Путь к зашифрованному файлу
            output_path: Путь для сохранения расшифрованного файла
            private_key_path: Путь к приватному RSA ключу
            encrypted_key_path: Путь к зашифрованному ключу Blowfish
        """
        priv = self.rsa.load_private(private_key_path)
        encrypted_sym = read_bytes(encrypted_key_path)
        sym_key = self.rsa.decrypt(priv, encrypted_sym)
        encrypted_data = read_bytes(input_path)
        decrypted_data = self.blowfish.decrypt(sym_key, encrypted_data)
        write_bytes(output_path, decrypted_data)
        print(f"Файл расшифрован: {output_path}")