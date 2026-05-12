import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

import symmetric
import asymmetric
import utils



def load_private_key(private_pem_path: str):
    """
        Загружает закрытый ключ RSA из файла
        Принимает: Путь к PEM-файлу закрытого ключа
        Возвращает: Объект закрытого ключа RSA
    """
    try:
        private_bytes = utils.read_bytes(private_pem_path)
        return load_pem_private_key(private_bytes, password=None)
    except ValueError:
        raise ValueError("Файл закрытого ключа имеет неверный формат или зашифрован.")

def generate_keys(path_to_cyph: str, path_to_public_key: str, path_to_private_key: str):
    """
        Генерирует ключи IDEA и RSA, шифрует IDEA-ключ и сохраняет их в файлы
        Принимает: Путь для сохранения зашифрованного ключа IDEA, путь для открытого ключа RSA, путь к файлу закрытого ключа RSA
        Возвращает: ничего, сохраняет файлы
    """
    try:
        idea_key = symmetric.generate_idea_key()
        private_key, public_key = asymmetric.generate_rsa_keypair()

        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        utils.save_to_dir(path_to_public_key, 'public.pem', public_bytes)

        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        utils.save_to_file(path_to_private_key, private_bytes)

        encrypted_idea_key = asymmetric.encrypt_idea_key_rsa(idea_key, public_key)
        utils.save_to_dir(path_to_cyph, 'symmetric_encrypted.txt', encrypted_idea_key)

        print("Ключи успешно сгенерированы и записаны в файлы!")

    except Exception as e:
        print(f"Непредвиденная ошибка при генерации ключей: {e}")

def encrypt_message(path_to_message: str, private_pem: str, path_to_cyph_key: str, path_to_save: str):
    """
        Шифрует текстовое сообщение гибридным методом (IDEA + RSA)
        Принимает: Путь к исходному сообщению, путь к закрытому ключу RSA, путь к зашифрованному ключу IDEA, путь для сохранения результата
        Возвращает: сохраняет зашифрованный файл
    """
    try:
        text = utils.read_bytes(path_to_message)
        c_text = utils.read_bytes(path_to_cyph_key)

        d_private_key = load_private_key(private_pem)
        dc_key = asymmetric.decrypt_idea_key_rsa(c_text, d_private_key)

        iv, cyph_text = symmetric.encrypt_data_idea(text, dc_key)

        os.makedirs(path_to_save, exist_ok=True)
        filename = utils.save_to_dir(path_to_save, "encrypted.txt", iv + cyph_text)

        print(f"Зашифрованный текст успешно сохранен: {filename}")

    except FileNotFoundError as e:
        print(f"Ошибка: Не найден файл {e.filename}")
    except ValueError as e:
        print(f"Криптографическая ошибка: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка при шифровании: {e}")

def decrypt_text(path_to_message: str, private_pem: str, path_to_cyph_key: str, path_to_save: str):
    """
        Расшифровывает текстовое сообщение гибридным методом
        Принимает: Путь к зашифрованному сообщению, путь к закрытому ключу RSA, путь к зашифрованному ключу IDEA, путь для сохранения результата
        Возвращает: сохраняет расшифрованный файл
    """
    try:
        combined_data = utils.read_bytes(path_to_message)

        if len(combined_data) < 8:
            raise ValueError("Файл слишком мал: отсутствует вектор инициализации (IV).")

        c_text = utils.read_bytes(path_to_cyph_key)

        d_private_key = load_private_key(private_pem)
        
        iv = combined_data[:8]
        actual_cyph_text = combined_data[8:]

        dc_key = asymmetric.decrypt_idea_key_rsa(c_text, d_private_key)
        unpadded_dc_text = symmetric.decrypt_data_idea(actual_cyph_text, iv, dc_key)

        print("Расшифрованный текст:\n", unpadded_dc_text.decode('UTF-8', errors='replace'))

        filename = utils.save_to_dir(path_to_save, 'decrypted.txt', unpadded_dc_text)
          
        print(f"Расшифрованный текст успешно сохранен: {filename}")

    except FileNotFoundError as e:
        print(f"Ошибка: Не найден файл {e.filename}")
    except ValueError as e:
        print(f"Криптографическая ошибка: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка при расшифровке: {e}")