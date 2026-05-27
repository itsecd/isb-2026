import os

from cryptography.hazmat.primitives import (
    hashes,
    padding as sym_padding,
    serialization
)

from cryptography.hazmat.primitives.asymmetric import (
    padding as asym_padding,
    rsa
)

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)


# FILES
def read_bytes(path):
    with open(path, "rb") as file:
        return file.read()


def write_bytes(path, data):

    folder = os.path.dirname(path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, "wb") as file:
        file.write(data)


# IDEA KEY
def generate_idea_key():

    # IDEA = 128 бит = 16 байт
    return os.urandom(16)


# RSA
def generate_rsa_keys():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


def save_private_key(private_key, path):

    data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    write_bytes(path, data)


def save_public_key(public_key, path):

    data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    write_bytes(path, data)


def load_private_key(path):

    return serialization.load_pem_private_key(
        read_bytes(path),
        password=None
    )


# RSA ENCRYPT IDEA KEY
def encrypt_symmetric_key(idea_key, public_key):

    return public_key.encrypt(
        idea_key,

        asym_padding.OAEP(
            mgf=asym_padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_symmetric_key(encrypted_key, private_key):

    return private_key.decrypt(
        encrypted_key,

        asym_padding.OAEP(
            mgf=asym_padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),
            label=None
        )
    )


# GENERATE KEYS
def generate_keys(
        encrypted_key_path,
        public_key_path,
        private_key_path
):

    print("[1/4] Генерация IDEA ключа...")

    idea_key = generate_idea_key()

    print("[2/4] Генерация RSA ключей...")

    private_key, public_key = generate_rsa_keys()

    print("[3/4] Сохранение RSA ключей...")

    save_private_key(private_key, private_key_path)
    save_public_key(public_key, public_key_path)

    print("[4/4] Шифрование IDEA ключа RSA...")

    encrypted_key = encrypt_symmetric_key(
        idea_key,
        public_key
    )

    write_bytes(encrypted_key_path, encrypted_key)

    print("Готово: ключи созданы")


# ENCRYPT FILE
def encrypt_file(
        input_path,
        private_key_path,
        encrypted_key_path,
        output_path
):

    print("[+] Загрузка RSA private key...")

    private_key = load_private_key(
        private_key_path
    )

    print("[+] Загрузка encrypted IDEA key...")

    encrypted_key = read_bytes(
        encrypted_key_path
    )

    print("[+] RSA дешифрование IDEA ключа...")

    idea_key = decrypt_symmetric_key(
        encrypted_key,
        private_key
    )

    print("[+] Чтение input.txt...")

    data = read_bytes(input_path)

    print("[+] Padding данных...")

    # IDEA block = 64 bits
    padder = sym_padding.PKCS7(64).padder()

    padded_data = (
            padder.update(data)
            + padder.finalize()
    )

    print("[+] Генерация IV...")

    # IDEA block size = 8 bytes
    iv = os.urandom(8)

    print("[+] IDEA-CBC шифрование...")

    cipher = Cipher(
        algorithms.IDEA(idea_key),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()

    encrypted_data = (
            encryptor.update(padded_data)
            + encryptor.finalize()
    )

    print("[+] Сохранение encrypted_data.bin...")

    write_bytes(
        output_path,
        iv + encrypted_data
    )

    print("Готово: файл зашифрован")


# DECRYPT FILE
def decrypt_file(
        input_path,
        private_key_path,
        encrypted_key_path,
        output_path
):

    print("[+] Загрузка RSA private key...")

    private_key = load_private_key(
        private_key_path
    )

    print("[+] Загрузка encrypted IDEA key...")

    encrypted_key = read_bytes(
        encrypted_key_path
    )

    print("[+] RSA дешифрование IDEA ключа...")

    idea_key = decrypt_symmetric_key(
        encrypted_key,
        private_key
    )

    print("[+] Чтение encrypted_data.bin...")

    data = read_bytes(input_path)

    iv = data[:8]

    encrypted_data = data[8:]

    print("[+] IDEA-CBC дешифрование...")

    cipher = Cipher(
        algorithms.IDEA(idea_key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    padded_data = (
            decryptor.update(encrypted_data)
            + decryptor.finalize()
    )

    print("[+] Удаление padding...")

    unpadder = sym_padding.PKCS7(64).unpadder()

    decrypted_data = (
            unpadder.update(padded_data)
            + unpadder.finalize()
    )

    print("[+] Сохранение output.txt...")

    write_bytes(output_path, decrypted_data)

    print("Готово: файл расшифрован")