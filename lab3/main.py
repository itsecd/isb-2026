import os
import json
import argparse
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

def log(msg):
    print(msg)

def read_conf(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        log(f"Ошибка: файл {path} не найден")
        sys.exit(1)
    except json.JSONDecodeError:
        log(f"Ошибка: файл {path} содержит некорректный JSON")
        sys.exit(1)

def gen_sym_key(bits):
    log(f"\nГенерация симметричного ключа AES ({bits} бит)")
    key = os.urandom(bits // 8)
    log("Симметричный ключ сгенерирован")
    return key

def gen_asym_keys():
    log("\nГенерация пары ключей RSA (2048 бит)")
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        log("Пара ключей RSA сгенерирована")
        return private_key, public_key
    except Exception as e:
        log(f"Ошибка при генерации RSA ключей: {e}")
        sys.exit(1)

def save_asym_keys(private_key, public_key, priv_path, pub_path):
    log(f"\nСохранение открытого ключа в {pub_path}")
    try:
        with open(pub_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    except IOError as e:
        log(f"Ошибка при сохранении открытого ключа: {e}")
        sys.exit(1)
    
    log(f"Сохранение закрытого ключа в {priv_path}")
    try:
        with open(priv_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    except IOError as e:
        log(f"Ошибка при сохранении закрытого ключа: {e}")
        sys.exit(1)
    
    log("Ключи RSA сохранены")

def enc_sym_key(sym_key, public_key, path):
    log("\nШифрование симметричного ключа с помощью RSA")
    try:
        encrypted = public_key.encrypt(
            sym_key,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        log(f"Ошибка при шифровании ключа: {e}")
        sys.exit(1)
    
    log(f"Сохранение зашифрованного ключа в {path}")
    try:
        with open(path, 'wb') as f:
            f.write(encrypted)
    except IOError as e:
        log(f"Ошибка при сохранении зашифрованного ключа: {e}")
        sys.exit(1)
    
    log("Симметричный ключ зашифрован")

def dec_sym_key(path, private_key):
    log(f"\nЧтение зашифрованного ключа из {path}")
    try:
        with open(path, 'rb') as f:
            encrypted = f.read()
    except FileNotFoundError:
        log(f"Ошибка: файл {path} не найден")
        sys.exit(1)
    except IOError as e:
        log(f"Ошибка при чтении файла {path}: {e}")
        sys.exit(1)
    
    log("Расшифровка симметричного ключа")
    try:
        sym_key = private_key.decrypt(
            encrypted,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        log(f"Ошибка при расшифровке ключа: {e}")
        sys.exit(1)
    
    log("Симметричный ключ расшифрован")
    return sym_key

def enc_file_aes(in_path, out_path, sym_key):
    log(f"\nЧтение файла {in_path}")
    try:
        with open(in_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        log(f"Ошибка: файл {in_path} не найден")
        sys.exit(1)
    except IOError as e:
        log(f"Ошибка при чтении файла {in_path}: {e}")
        sys.exit(1)
    
    iv = os.urandom(16)
    log("Сгенерирован IV")
    
    try:
        padder = padding.ANSIX923(128).padder()
        padded_data = padder.update(data) + padder.finalize()
    except Exception as e:
        log(f"Ошибка при паддинге: {e}")
        sys.exit(1)
    
    log("Паддинг добавлен")
    
    try:
        cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    except Exception as e:
        log(f"Ошибка при шифровании AES: {e}")
        sys.exit(1)
    
    log("Данные зашифрованы")
    
    log(f"Сохранение в {out_path}")
    try:
        with open(out_path, 'wb') as f:
            f.write(iv + ciphertext)
    except IOError as e:
        log(f"Ошибка при сохранении файла: {e}")
        sys.exit(1)
    
    log("Файл сохранён")

def dec_file_aes(in_path, out_path, sym_key):
    log(f"\nЧтение файла {in_path}")
    try:
        with open(in_path, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()
    except FileNotFoundError:
        log(f"Ошибка: файл {in_path} не найден")
        sys.exit(1)
    except IOError as e:
        log(f"Ошибка при чтении файла {in_path}: {e}")
        sys.exit(1)
    
    log("Расшифровка данных AES")
    try:
        cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as e:
        log(f"Ошибка при расшифровке AES: {e}")
        sys.exit(1)
    
    log("Удаление паддинга")
    try:
        unpadder = padding.ANSIX923(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
    except Exception as e:
        log(f"Ошибка при удалении паддинга: {e}")
        sys.exit(1)
    
    log(f"Сохранение в {out_path}")
    try:
        with open(out_path, 'wb') as f:
            f.write(data)
    except IOError as e:
        log(f"Ошибка при сохранении файла: {e}")
        sys.exit(1)
    
    log("Файл сохранён")

def generation(config_path):
    log("\nРежим генерации ключей")
    conf = read_conf(config_path)
    
    bits = conf.get('symmetric_key_size_bits', 256)
    if bits not in [128, 192, 256]:
        log(f"Неправильная длина ключа {bits}, будет использованн 256")
        bits = 256
    
    sym_key = gen_sym_key(bits)
    priv_key, pub_key = gen_asym_keys()
    save_asym_keys(priv_key, pub_key, conf['private_key'], conf['public_key'])
    enc_sym_key(sym_key, pub_key, conf['encrypted_symmetric_key'])
    
    log("\nГенерация завершена\n")

def encryption(config_path):
    log("\nРежим шифрования")
    conf = read_conf(config_path)
    
    log(f"\nЗагрузка закрытого ключа из {conf['private_key']}")
    try:
        with open(conf['private_key'], 'rb') as f:
            priv_key = load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        log(f"Ошибка: файл {conf['private_key']} не найден")
        sys.exit(1)
    except ValueError as e:
        log(f"Ошибка: некорректный ключ - {e}")
        sys.exit(1)
    except Exception as e:
        log(f"Ошибка при загрузке ключа: {e}")
        sys.exit(1)
    
    log("Закрытый ключ загружен")
    
    sym_key = dec_sym_key(conf['encrypted_symmetric_key'], priv_key)
    enc_file_aes(conf['initial_file'], conf['encrypted_file'], sym_key)
    
    log("\nШифрование завершено\n")

def decryption(config_path):
    log("\nРежим дешифрования")
    conf = read_conf(config_path)
    
    log(f"\nЗагрузка закрытого ключа из {conf['private_key']}")
    try:
        with open(conf['private_key'], 'rb') as f:
            priv_key = load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        log(f"Ошибка: файл {conf['private_key']} не найден")
        sys.exit(1)
    except ValueError as e:
        log(f"Ошибка: некорректный ключ - {e}")
        sys.exit(1)
    except Exception as e:
        log(f"Ошибка при загрузке ключа: {e}")
        sys.exit(1)
    
    log("Закрытый ключ загружен")
    
    sym_key = dec_sym_key(conf['encrypted_symmetric_key'], priv_key)
    dec_file_aes(conf['encrypted_file'], conf['decrypted_file'], sym_key)
    
    log("\nДешифрование завершено\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Гибридная криптосистема AES+RSA')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', 
                       help='Режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true',
                       help='Режим шифрования')
    group.add_argument('-dec', '--decryption', action='store_true',
                       help='Режим дешифрования')
    parser.add_argument('config', help='Путь к конфигурационному JSON-файлу')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(1)
    
    if args.generation:
        generation(args.config)
    elif args.encryption:
        encryption(args.config)
    elif args.decryption:
        decryption(args.config)