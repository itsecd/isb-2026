"""
Модуль гибридной криптосистемы, сочетающей RSA и Blowfish.

Гибридное шифрование использует преимущества обоих алгоритмов:
- RSA для безопасной передачи симметричного ключа
- Blowfish для быстрого шифрования данных
"""

import argparse
import rsa_operations
import blowfish_cipher
import file_handler
import key_factory


def parsing() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    
    Returns:
        argparse.Namespace: Объект с аргументами командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема (RSA + Blowfish)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generator', action='store_true', help="Режим генерации ключей")
    group.add_argument('-enc', '--encryption', action='store_true', help="Режим шифрования данных")
    group.add_argument('-dec', '--decryption', action='store_true', help="Режим дешифрования данных")
    parser.add_argument("--enc_key", type=str, help="Путь к зашифрованному симметричному ключу")
    parser.add_argument("--rsa_pri_key", type=str, help="Путь к закрытому ассимметричному ключу")
    parser.add_argument("--rsa_pub_key", type=str, help="Путь к открытому ассимметричному ключу")
    parser.add_argument("--enc_text", type=str, help="Путь для сохранения(доступа) к зашифрованному тексту")
    parser.add_argument("--dec_text", type=str, help="Путь к расшифрованному тексту")
    parser.add_argument("--init_text", type=str, help="Путь к шифруемому текстовому файлу")
    parser.add_argument("--len_key", type=str, help="Длина ключа")
    parser.add_argument("--config", type=str, nargs='?', default="config.json", help="Путь к файлу настроек(по умолчанию config.json)")
    return parser.parse_args()


def initialize_configuration() -> dict:
    """
    Инициализация конфигурации системы.
    
    Returns:
        dict: Словарь с конфигурационными параметрами.
    """
    args = parsing()
    config_data = file_handler.read_config(args.config)

    configuration = {
        'operation_mode': 'generate' if args.generator else 'encrypt' if args.encryption else 'decrypt',
        'input_file': args.init_text or config_data.get("source_file"),
        'encrypted_output': args.enc_text or config_data.get("output_encrypted"),
        'decrypted_output': args.dec_text or config_data.get("output_decrypted"),
        'session_key_file': args.enc_key or config_data.get("encrypted_session_key"),
        'public_key_file': args.rsa_pub_key or config_data.get("rsa_public_key"),
        'private_key_file': args.rsa_pri_key or config_data.get("rsa_private_key"),
        'symmetric_key_size': args.len_key or config_data.get("key_length"),
    }
    return configuration


def execute_key_generation(config: dict) -> None:
    """
    Выполнение процедуры генерации ключей.
    
    Args:
        config: Словарь с конфигурационными параметрами.
    """
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
    """
    Выполнение процедуры шифрования.
    
    Args:
        config: Словарь с конфигурационными параметрами.
    """
    print("Запуск шифрования данных...")
    rsa_private = file_handler.retrieve_rsa_private_key(config['private_key_file'])
    encrypted_session_key = file_handler.retrieve_symmetric_key(config['session_key_file'])
    session_key = rsa_operations.decrypt_session_key(rsa_private, encrypted_session_key)
    source_text = file_handler.load_plaintext(config['input_file'])
    encrypted_data = blowfish_cipher.encrypt_message(session_key, source_text)
    file_handler.save_binary_data(encrypted_data, config['encrypted_output'])
    print("Данные успешно зашифрованы.")


def execute_decryption(config: dict) -> None:
    """
    Выполнение процедуры расшифровки.
    
    Args:
        config: Словарь с конфигурационными параметрами.
    """
    print("Запуск расшифровки данных...")
    rsa_private = file_handler.retrieve_rsa_private_key(config['private_key_file'])
    encrypted_session_key = file_handler.retrieve_symmetric_key(config['session_key_file'])
    session_key = rsa_operations.decrypt_session_key(rsa_private, encrypted_session_key)
    encrypted_data = file_handler.load_binary_data(config['encrypted_output'])
    decrypted_text = blowfish_cipher.decrypt_message(session_key, encrypted_data)
    file_handler.save_plaintext(decrypted_text, config['decrypted_output'])
    print("Данные успешно расшифрованы.")


def main() -> None:
    """
    Точка входа в приложение.
    """
    configuration = initialize_configuration()
    match configuration['operation_mode']:
        case 'generate':
            execute_key_generation(configuration)
        case 'encrypt':
            execute_encryption(configuration)
        case 'decrypt':
            execute_decryption(configuration)


if __name__ == "__main__":
    main()