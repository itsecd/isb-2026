import argparse
import sys

from auxiliary_functions import load_settings
from asymmetrical import generate_rsa_keys, save_rsa_keys, encrypt_symmetric_key, decrypt_symmetric_key
from symmetrical import generate_symmetric_key, encrypt_data, decrypt_data

def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gen', action='store_true', help='Генерация ключей')
    group.add_argument('--enc', action='store_true', help='Шифрование данных')
    group.add_argument('--dec', action='store_true', help='Дешифрование данных')
    
    parser.add_argument('--settings', type=str, default='settings.json', help='Путь к файлу настроек JSON')

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    try:
        settings = load_settings(args.settings)
    except Exception as e:
        print(f"Ошибка при загрузке настроек: {e}")
        sys.exit(1)

    if settings is None:
        print("Не удалось загрузить настройки. Проверьте файл settings.json.")
        sys.exit(1)

    match True:
        case _ if args.gen:
            try:
                symmetric_key = generate_symmetric_key(settings)
                if symmetric_key is None:
                    print("Ошибка: Не удалось сгенерировать симметричный ключ.")
                    sys.exit(1)
                
                private_key, public_key = generate_rsa_keys(settings)
                if private_key is None or public_key is None:
                    print("Ошибка: Не удалось сгенерировать пару RSA ключей.")
                    sys.exit(1)
                
                if not save_rsa_keys(settings, private_key, public_key):
                    print("Ошибка: Не удалось сохранить RSA ключи на диск.")
                    sys.exit(1)
                
                encrypted_sym_key = encrypt_symmetric_key(settings, symmetric_key)
                if encrypted_sym_key is None:
                    print("Ошибка: Не удалось зашифровать симметричный ключ.")
                    sys.exit(1)
                
                print("Генерация ключей завершена успешно.")
                
            except Exception as e:
                print(f"Ошибка при генерации ключей: {e}")
                sys.exit(1)
            
        case _ if args.enc:
            try:
                symmetric_key = decrypt_symmetric_key(settings)
                if symmetric_key is None:
                    print("Ошибка: Не удалось расшифровать симметричный ключ. Проверьте наличие private_key и encrypted_symmetric_key.")
                    sys.exit(1)
                print("Симметричный ключ успешно расшифрован.")
                
                success = encrypt_data(settings, symmetric_key)
                if not success:
                    print("Ошибка: Процесс шифрования данных завершился неудачно.")
                    sys.exit(1)
                    
                print("Процесс шифрования завершен успешно.")

            except FileNotFoundError as e:
                print(f"Ошибка доступа к файлам: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Ошибка при шифровании: {e}")
                sys.exit(1)
                
        case _ if args.dec:
            try:
                symmetric_key = decrypt_symmetric_key(settings)
                if symmetric_key is None:
                    print("Ошибка: Не удалось расшифровать симметричный ключ. Проверьте наличие private_key и encrypted_symmetric_key.")
                    sys.exit(1)
                print("Симметричный ключ успешно расшифрован.")
                
                success = decrypt_data(settings, symmetric_key)
                if not success:
                    print("Ошибка: Процесс дешифрования данных завершился неудачно. Возможно, ключ неверен или файл поврежден.")
                    sys.exit(1)
                    
                print("Процесс дешифрования завершен успешно.")

            except FileNotFoundError as e:
                print(f"Ошибка доступа к файлам: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Ошибка при дешифровании: {e}")
                sys.exit(1)

if __name__ == '__main__':
    main()