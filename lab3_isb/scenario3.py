from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives import hashes   
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from utilits import decrypt_symmetric_key
from files import load_private_key, load_ciphertext, read_binary, save_binary

    


def text_decrypt(enc_txt: bytes, key: bytes) -> bytes:
    """
    Дешифрование данных симметричным алгоритмом AES-CBC.
    :param enc_txt: зашифрованные данные в виде байтов; первые 16 байт содержат IV
    :param key: симметричный AES-ключ
    :return: расшифрованные данные в виде байтов
    """

    if len(enc_txt) < 16:
        raise ValueError("Ciphertext is too short to contain IV")
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 128, 192, 256 bits long")
    iv = enc_txt[:16]
    ciphertext = enc_txt[16:]
    if len(ciphertext) % 16 != 0 or len(ciphertext) == 0:
        raise ValueError("Invalid ciphertext length")
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv)) 
    decryptor = cipher.decryptor()
    unpadder = sym_padding.ANSIX923(128).unpadder()
    padded_text  = decryptor.update(ciphertext) + decryptor.finalize()
    text = unpadder.update(padded_text) + unpadder.finalize()
    return text



def run_scenario3(enc_txt_path: str, prv_asym_key_path: str, enc_key_path: str, dec_txt_path: str) -> None:
    """
    Запуск сценария дешифрования данных.
    :param enc_txt_path: путь к зашифрованному текстовому файлу
    :param prv_asym_key_path: путь к закрытому RSA-ключу
    :param enc_key_path: путь к файлу с зашифрованным симметричным AES-ключом
    :param dec_txt_path: путь для сохранения расшифрованного текстового файла
    :return: не возвращается
    """

    enc_txt = load_ciphertext(enc_txt_path)
    private_key = load_private_key(prv_asym_key_path)
    enc_key = read_binary(enc_key_path)
    decrypted_key = decrypt_symmetric_key(enc_key, private_key)
    decrypted_text = text_decrypt(enc_txt, decrypted_key)
    save_binary(decrypted_text, dec_txt_path)
    print(f"Scenario 3 completed successfully. Encrypted text from {enc_txt_path} decrypted and saved to {dec_txt_path}.")



