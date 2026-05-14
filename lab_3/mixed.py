from blowfish import generate_blowfish_key
from rsa import generate_key_pair, save_public_key, save_private_key, encrypt_rsa, load_private_key, decrypt_rsa
from blowfish import encrypt_blowfish


def generate_keys(settings: dict) -> None:
    """
    Generate RSA and Blowfish keys.
    :param settings: json-settings
    """
    key_length = settings['symmetric_key_length']
    symmetric_key = generate_blowfish_key(key_length)

    private_key, public_key = generate_key_pair()

    save_private_key(private_key, settings['secret_key'])
    save_public_key(public_key, settings['public_key'])

    encrypted_symmetric_key = encrypt_rsa(public_key, symmetric_key)
    with open(settings['symmetric_key'], 'wb') as file:
        file.write(encrypted_symmetric_key)


def get_symmetric_key(settings: dict) -> bytes:
    """
    Help function to decrypt and pass symmetric key.
    :param settings: json-settings
    :return: symmetric key
    """
    private_key = load_private_key(settings['secret_key'])
    with open(settings['symmetric_key'], mode='rb') as key_file:
        encrypted_symmetric_key = key_file.read()
    with open(settings['initial_file'], 'rb') as initial_file:
        data = initial_file.read()
    return decrypt_rsa(private_key, encrypted_symmetric_key)


def encrypt_data(settings: dict) -> None:
    """
    Load, encrypt with Blowfish and save data.
    :param settings: json-settings
    """
    symmetric_key = get_symmetric_key(settings)
    with open(settings['initial_file'], 'rb') as initial_file:
        data = initial_file.read()
    encrypted_data = encrypt_blowfish(symmetric_key, data)
    with open(settings['encrypted_file'], 'wb') as file:
        file.write(encrypted_data)


def decrypt_data(settings: dict) -> None:
    """
    Load, dencrypt with Blowfish and save data.
    :param settings: json-settings
    """
    symmetric_key = get_symmetric_key(settings)
    with open(settings['encrypted_file'], 'rb') as initial_file:
        data = initial_file.read()
    decrypted_data = encrypt_blowfish(symmetric_key, data)
    with open(settings['decrypted_file'], 'wb') as file:
        file.write(decrypted_data)
