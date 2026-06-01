import argparse
import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding


def load_settings(json_path="settings.json"):
    if os.path.exists(json_path):
        with open(json_path,'r') as f:
            return json.load(f)
    return {}

def save_bin_data(data,path):
    with open(path, "wb") as f:
        f.write(data)
    
def load_bin_data(path):
    with open(path, "rb") as f:
        return f.read()

def generate_keys(len_bits, pub_key_path, priv_key_path,enc_key_path):
    if len_bits == 64:

        print("Это ты че захотел? Поюзать удаленные алгоритмы? энивей будет 16 байт, lox")
        key_len_bytes = 16 
    elif len_bits == 128:
        key_len_bytes = 16
        algo_name = "3DES (2-key)"
    elif len_bits == 192:
        key_len_bytes = 24
        algo_name = "3DES (3-key)"
    else:
        raise ValueError("Выберите 64, 128 или 192, балда")
    
    sym_key = os.urandom(key_len_bytes)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    save_bin_data(private_pem, priv_key_path)
    
    
    public_key = private_key.public_key()
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    save_bin_data(public_pem, pub_key_path)
    
    encrypted_sym_key = public_key.encrypt(
        sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    save_bin_data(encrypted_sym_key, enc_key_path)
    
def get_algo(sym_key):
    if len(sym_key) == 8:
        return algorithms.DES(sym_key)
    elif len(sym_key) in (16, 24):
        return algorithms.TripleDES(sym_key)
    else:
        raise ValueError("Неверная длина, оболдуй") 
    
def encrypt_data(input_path, priv_key_path, enc_key_path, output_path):
    
    private_pem = load_bin_data(priv_key_path)
    private_key = serialization.load_pem_private_key(private_pem,password=None)
    
    encrypted_sym_key = load_bin_data(enc_key_path)
    sym_key = private_key.decrypt(
        encrypted_sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    plaintext = load_bin_data(input_path)
    
    block_size = 8 
    iv = os.urandom(block_size)
    
    padder = padding.ANSIX923(block_size*8).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher_algo = get_algo(sym_key)
    
    cipher = Cipher(cipher_algo, modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    
    final_output = iv + cipher_text
    save_bin_data(final_output, output_path)
    
    
def decrypt_data(input_path, priv_key_path, enc_key_path, output_path):
    private_pem = load_bin_data(priv_key_path)
    private_key = serialization.load_pem_private_key(private_pem,password=None)
    
    encrypted_sym_key = load_bin_data(enc_key_path)
    sym_key = private_key.decrypt(
        encrypted_sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    encrypted_content = load_bin_data(input_path)
    block_size = 8
    if len(encrypted_content) < block_size:
        raise ValueError("ну все, потеря-потерь.")
    
    iv = encrypted_content[:block_size]
    ciphertext = encrypted_content[block_size:]
    
    cipher_algo = get_algo(sym_key)
    cipher = Cipher(cipher_algo,modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.ANSIX923(32).unpadder()
    unpadded_dc_text = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    save_bin_data(unpadded_dc_text, output_path)
    
def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема (RSA + DES/3DES)")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generate', action='store_true', help='Режим генерации ключей')
    group.add_argument('-enc', '--encrypt', action='store_true', help='Режим шифрования')
    group.add_argument('-dec', '--decrypt', action='store_true', help='Режим дешифрования')


    parser.add_argument('--key-len', type=int, choices=[64, 128, 192], default=192, help='Длина симметричного ключа в битах (только для генерации)')
    parser.add_argument('--pub-key', type=str, help='Путь для открытого ключа')
    parser.add_argument('--priv-key', type=str, help='Путь для закрытого ключа')
    parser.add_argument('--enc-sym-key', type=str, help='Путь для зашифрованного симметричного ключа')


    parser.add_argument('--input', type=str, help='Входной файл (текст для шифрования или шифротекст для расшифровки)')
    parser.add_argument('--output', type=str, help='Выходной файл')
    

    parser.add_argument('--loaded-priv-key', type=str, help='Путь к закрытому ключу RSA (для расшифровки симметричного ключа)')
    parser.add_argument('--loaded-enc-sym-key', type=str, help='Путь к зашифрованному симметричному ключу')

    args = parser.parse_args()
    
    settings = load_settings()
    
    def get_path(cli_arg, setting_key, default_val):
        if cli_arg:
            return cli_arg
        if setting_key in settings:
            return settings[setting_key]
        return default_val
    
    if args.generate:
        pub_key_path = get_path(args.pub_key, 'public_key', 'public.pem')
        priv_key_path = get_path(args.priv_key, 'secret_key', 'private.pem')
        enc_sym_key_path = get_path(args.enc_sym_key, 'symmetric_key_encrypted', 'sym_key.enc')
        
        generate_keys(args.key_len, pub_key_path, priv_key_path, enc_sym_key_path)

    elif args.encrypt:
        input_path = get_path(args.input, 'initial_file', 'input.txt')
        output_path = get_path(args.output, 'encrypted_file', 'output.enc')
        priv_key_path = get_path(args.loaded_priv_key, 'secret_key', 'private.pem')
        enc_sym_key_path = get_path(args.loaded_enc_sym_key, 'symmetric_key_encrypted', 'sym_key.enc')

        encrypt_data(input_path, priv_key_path, enc_sym_key_path, output_path)

    elif args.decrypt:
        input_path = get_path(args.input, 'encrypted_file', 'output.enc')
        output_path = get_path(args.output, 'decrypted_file', 'decrypted.txt')
        priv_key_path = get_path(args.loaded_priv_key, 'secret_key', 'private.pem')
        enc_sym_key_path = get_path(args.loaded_enc_sym_key, 'symmetric_key_encrypted', 'sym_key.enc')

        decrypt_data(input_path, priv_key_path, enc_sym_key_path, output_path)

if __name__ == '__main__':
    main()
    
#python python.py --generate --key-len 128 --pub-key public.pem --priv-key private.pem --enc-sym-key sym_key.enc
#python python.py --encrypt --input input.txt --output output.enc --loaded-priv-key private.pem --loaded-enc-sym-key sym_key.enc
#python python.py --decrypt --input output.enc --output decrypted.txt --loaded-priv-key private.pem --loaded-enc-sym-key sym_key.enc