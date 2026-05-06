import asymmetrical
import symmetrical
import so


def generate_key_mode(en_sym_path: str, private_path: str) -> None:
    """
    Генерирует новую пару RSA-ключей и симметричный ключ, сохраняя их в файлы.

    Симметричный ключ шифруется открытым ключом RSA перед сохранением.

    Args:
        en_sym_path (str): Путь для сохранения зашифрованного симметричного ключа.
        private_path (str): Путь для сохранения приватного ключа RSA.
    """
    sym_key = symmetrical.generate_sym_key()
    private_key, public_key = asymmetrical.generate_rsa_keys()

    en_sym_key = asymmetrical.encrypt_sym_key(sym_key, public_key)

    so.save_binary(en_sym_path, en_sym_key)
    so.save_private_key(private_path, private_key)
    print("Ключи сгенерированы и сохранены")


def encrypt_data_mode(input_path: str, output_path: str, sym_path: str, private_path: str) -> None:
    """
    Шифрует файл, используя существующие ключи.

    Сначала расшифровывает симметричный ключ с помощью приватного RSA-ключа, 
    затем шифрует данные симметричным алгоритмом.

    Args:
        input_path (str): Путь к исходному файлу с данными.
        output_path (str): Путь для сохранения зашифрованного файла.
        sym_path (str): Путь к зашифрованному симметричному ключу.
        private_path (str): Путь к приватному ключу RSA.
    """
    private_key = so.open_private_key(private_path)
    enc_sym_key = so.open_binary(sym_path)

    sym_key = asymmetrical.decrypt_sym_key(enc_sym_key, private_key)

    d_data = so.open_binary(input_path)
    e_data = symmetrical.encryption_data(d_data, sym_key)

    so.save_binary(output_path, e_data)
    print("Данные успешно зашифрованы")


def decrypt_data_mode(input_path: str, output_path: str, sym_path: str, private_path: str) -> None:
    """
    Расшифровывает файл, используя приватный RSA-ключ и зашифрованный симметричный ключ.

    Args:
        input_path (str): Путь к зашифрованному файлу.
        output_path (str): Путь для сохранения расшифрованного файла.
        sym_path (str): Путь к зашифрованному симметричному ключу.
        private_path (str): Путь к приватному ключу RSA.
    """
    private_key = so.open_private_key(private_path)
    enc_sym_key = so.open_binary(sym_path)

    sym_key = asymmetrical.decrypt_sym_key(enc_sym_key, private_key)

    e_data = so.open_binary(input_path)
    d_data = symmetrical.decryption_data(e_data, sym_key)

    so.save_binary(output_path, d_data)
    print("Данные успешно расшифрованы")


def encrypt_data_all_mode(en_sym_path: str, private_path: str, input_path: str, output_path: str) -> None:
    """
    Выполняет полный цикл: генерацию ключей и шифрование данных за один проход.

    Args:
        en_sym_path (str): Путь для сохранения нового зашифрованного симметричного ключа.
        private_path (str): Путь для сохранения нового приватного ключа RSA.
        input_path (str): Путь к исходным данным.
        output_path (str): Путь для сохранения зашифрованных данных.
    """
    sym_key = symmetrical.generate_sym_key()
    private_key, public_key = asymmetrical.generate_rsa_keys()

    en_sym_key = asymmetrical.encrypt_sym_key(sym_key, public_key)

    so.save_binary(en_sym_path, en_sym_key)
    so.save_private_key(private_path, private_key)

    d_data = so.open_binary(input_path)
    e_data = symmetrical.encryption_data(d_data, sym_key)

    so.save_binary(output_path, e_data)
    print("Ключи созданы, данные зашифрованы")
