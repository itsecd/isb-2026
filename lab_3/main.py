import argparse
import json
from key import (generate_symmetric_key, generate_asymmetric_keys, write_public_key, write_private_key, encrypt_symmetric_key, read_symmetric_key, read_private_pem, decrypt_symmetric_key)
from crypt import encrypt_text, decrypt_text
from file_func import read_text_file, write_encrypt_text, read_encrypt_text, write_decrypt_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-gen', '--generation', choices=['yes'], help='Запускает режим генерации ключей')
    parser.add_argument('-enc', '--encryption', choices=['yes'], help='Запускает режим шифрования')
    parser.add_argument('-dec', '--decryption', choices=['yes'], help='Запускает режим дешифрования')
    parser.add_argument('-json', '--settings', default='settings.json', help='путь к файлу с настройками')
    args = parser.parse_args()

    try:
        with open(args.settings, 'r') as json_file:
            json_data = json.load(json_file)

            initial_file = json_data['initial_file']
            encrypted_file = json_data['encrypted_file']
            decrypted_file = json_data['decrypted_file']
            symmetric_key_file = json_data['symmetric_key']
            public_key_file = json_data['public_key']
            secret_key_file = json_data['secret_key']
        print("Настройки загружены, всё норм")

    except FileNotFoundError:
        print("Кто-то съел файл с настройками")
        return
    except Exception as error:
        print(f"Произошла ошибка: {error}")
        return


    try:
        match (args.generation, args.encryption, args.decryption):
            case (str(), _, _):
                print("Запуск режима генерации ключей")
                
                key = generate_symmetric_key()
                print("1.1 Ключ для симметричного алгоритма сгенерирован")

                private_key, public_key = generate_asymmetric_keys()
                print("1.2 Ключи для асимметричного алгоритма сгенерированы")

                write_public_key(public_key, public_key_file)
                print("1.3.1 Публичный ключ загружен в .pem файл")
            
                write_private_key(private_key, secret_key_file)
                print("1.3.2 Приватный ключ загружен в .pem файл")
            
                encrypt_key = encrypt_symmetric_key(key, public_key)
                print("1.4.1 Симметричный ключ зашифрован публичным ключом")
            
                write_decrypt_text(encrypt_key, symmetric_key_file)
                print("1.4.2 Зашифрованный симметричный ключ сохранен в файл .txt")
            

            case (_, str(), _):
                print("Режим шифрования данных")
            
                content = read_symmetric_key(symmetric_key_file)
                print("2.1.1 Зашифрованный симметричный ключ считан из файла")
            
                private_key = read_private_pem(secret_key_file)
                print("2.1.2 Приватный ключ для расшифровки симметричного ключа считан из файла")
                
                key = decrypt_symmetric_key(content, private_key)
                print("2.1.3 Симметричный ключ расшифрован")
            
                text_bytes = read_text_file(initial_file)
                print("2.2.1 Текст для шифрования считан из файла")
            
                iv, c_text = encrypt_text(text_bytes, key)
                print("2.2.2 Текст зашифрован с использованием алгоритма SM4")
            
                write_encrypt_text(encrypted_file, iv, c_text)
                print("2.2.3 Зашифрованный текст записан в файл")

            

            case (_, _, str()):
                print("Режим расшифровки данных")
            
                content = read_symmetric_key(symmetric_key_file)
                print("3.1.1 Зашифрованный симметричный ключ считан из файла")
            
                private_key = read_private_pem(secret_key_file)
                print("3.1.2 Приватный ключ для расшифровки симметричного ключа считан из файла")
            
                key = decrypt_symmetric_key(content, private_key)
                print("3.1.3 Симметричный ключ расшифрован")
            
                iv, c_text = read_encrypt_text(encrypted_file)
                print("3.2.1 Зашифрованный текст считан из файла")
            
                dc_text = decrypt_text(iv, c_text, key)
                print("3.2.2 Текст расшифрован")
            
                write_decrypt_text(decrypted_file, dc_text)
                print("3.2.3 Расшифрованный текст записан в файл")

            case _:
                print("Ошибка: неверные параметры")
             
    except Exception as error:
        print(f"Произошла ошибка: {error}")

if __name__ == "__main__" :
    main()
