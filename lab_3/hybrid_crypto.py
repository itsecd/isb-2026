import argparse
import rsa_operations
import blowfish_cipher
import file_handler
import key_factory

def parse_arguments() -> argparse.Namespace:
    """Обработка аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема (RSA + Blowfish)"
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '-gen', '--generate-keys',
        action='store_true',
        help="Режим генерации ключей шифрования"
    )
    mode_group.add_argument(
        '-enc', '--encrypt',
        action='store_true',
        help="Режим шифрования данных"
    )
    mode_group.add_argument(
        '-dec', '--decrypt',
        action='store_true',
        help="Режим расшифровки данных"
    )

    parser.add_argument(
        "--session-key-path",
        type=str,
        help="Путь к зашифрованному сессионному ключу"
    )
    parser.add_argument(
        "--private-key-path",
        type=str,
        help="Путь к закрытому RSA ключу"
    )
    parser.add_argument(
        "--public-key-path",
        type=str,
        help="Путь к открытому RSA ключу"
    )
    parser.add_argument(
        "--ciphertext-path",
        type=str,
        help="Путь для сохранения/чтения зашифрованных данных"
    )
    parser.add_argument(
        "--plaintext-output",
        type=str,
        help="Путь для сохранения расшифрованного текста"
    )
    parser.add_argument(
        "--source-file",
        type=str,
        help="Путь к исходному текстовому файлу"
    )
    parser.add_argument(
        "--key-size",
        type=str,
        help="Размер симметричного ключа в битах"
    )
    parser.add_argument(
        "--config-file",
        type=str,
        nargs='?',
        default="config.json",
        help="Путь к конфигурационному файлу"
    )

    return parser.parse_args()

def initialize_configuration() -> dict:
    """Инициализация конфигурации системы"""
    args = parse_arguments()
    config_data = file_handler.read_config(args.config_file)

    configuration = {
        'operation_mode': 'generate' if args.generate_keys else 'encrypt' if args.encrypt else 'decrypt',
        'input_file': args.source_file or config_data.get("source_file"),
        'encrypted_output': args.ciphertext_path or config_data.get("output_encrypted"),
        'decrypted_output': args.plaintext_output or config_data.get("output_decrypted"),
        'session_key_file': args.session_key_path or config_data.get("encrypted_session_key"),
        'public_key_file': args.public_key_path or config_data.get("rsa_public_key"),
        'private_key_file': args.private_key_path or config_data.get("rsa_private_key"),
        'symmetric_key_size': args.key_size or config_data.get("key_length"),
    }
    
    return configuration

def execute_key_generation(config: dict) -> None:
    """Выполнение процедуры генерации ключей"""
    print("Запуск генерации ключей гибридной криптосистемы...")
    
    rsa_private, rsa_public = key_factory.create_rsa_keypair()
    
    symmetric_key = key_factory.create_symmetric_key(int(config['symmetric_key_size']))
    
    file_handler.store_asymmetric_keys(
        config['public_key_file'],
        config['private_key_file'],
        rsa_private,
        rsa_public
    )
    
    encrypted_session_key = rsa_operations.encrypt_session_key(rsa_public, symmetric_key)
    file_handler.store_symmetric_key(config['session_key_file'], encrypted_session_key)
    
    print("Ключи успешно сгенерированы и сохранены.")

def execute_encryption(config: dict) -> None:
    """Выполнение процедуры шифрования"""
    print("Запуск шифрования данных...")
    
    rsa_private = file_handler.retrieve_rsa_private_key(config['private_key_file'])
    encrypted_session_key = file_handler.retrieve_symmetric_key(config['session_key_file'])
    session_key = rsa_operations.decrypt_session_key(rsa_private, encrypted_session_key)
    
    source_text = file_handler.load_plaintext(config['input_file'])
    encrypted_data = blowfish_cipher.encrypt_message(session_key, source_text)
    
    file_handler.save_binary_data(encrypted_data, config['encrypted_output'])
    
    print("Данные успешно зашифрованы.")

def execute_decryption(config: dict) -> None:
    """Выполнение процедуры расшифровки"""
    print("Запуск расшифровки данных...")
    
    rsa_private = file_handler.retrieve_rsa_private_key(config['private_key_file'])
    encrypted_session_key = file_handler.retrieve_symmetric_key(config['session_key_file'])
    session_key = rsa_operations.decrypt_session_key(rsa_private, encrypted_session_key)
    
    encrypted_data = file_handler.load_binary_data(config['encrypted_output'])
    decrypted_text = blowfish_cipher.decrypt_message(session_key, encrypted_data)
    
    file_handler.save_plaintext(decrypted_text, config['decrypted_output'])
    
    print("Данные успешно расшифрованы.")

def main() -> None:
    """Точка входа в приложение"""
    configuration = initialize_configuration()

    if configuration['operation_mode'] == 'generate':
        execute_key_generation(configuration)
    elif configuration['operation_mode'] == 'encrypt':
        execute_encryption(configuration)
    elif configuration['operation_mode'] == 'decrypt':
        execute_decryption(configuration)

if __name__ == "__main__":
    main()