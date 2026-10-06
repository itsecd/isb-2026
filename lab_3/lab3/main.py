import time
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def r_check_txt(path_f: str) -> str:
    """Проверяет, что путь ведёт к существующему .txt файлу.
    Если расширение не .txt или файла нет — запрашивает путь заново.
    Возвращает корректный путь."""
    while True:
        if not path_f.lower().endswith(".txt"):
            path_f = input(f"path {path_f} does not lead to a .txt file. pls rewrite: ")
            continue
        if not os.path.isfile(path_f):
            path_f = input(f"file {path_f} doesn't exists, pls rewrite it?: ")
            continue
        return path_f

def r_check_pem(path_f: str) -> str:
    """Проверяет, что путь ведёт к существующему .pem файлу.
    Если расширение не .pem или файла нет — запрашивает путь заново.
    Возвращает корректный путь."""
    while True:
        if not path_f.lower().endswith(".pem"):
            path_f = input(f"path {path_f} does not lead to a .pem file. pls rewrite: ")
            continue
        if not os.path.isfile(path_f):
            path_f = input(f"file {path_f} doesn't exists, pls rewrite it: ")
            continue
        return path_f

def w_check_txt(path_f: str) -> str:
    """Проверяет путь для записи .txt файла.
    Требует расширение .txt; если файл уже существует — спрашивает,
    перезаписывать ли его. Возвращает подтверждённый путь."""
    while True:
        if not path_f.lower().endswith(".txt"):
            path_f = input(f"path {path_f} does not lead to a .txt file. pls rewrite: ")
            continue
        if os.path.isfile(path_f):
            ans = input(f"file {path_f} already exists, do you want to rewrite it?(y/n): ")
            if ans.lower() == 'n':
                path_f = input("then input new path: ")
                continue
            if ans.lower() == 'y':
                return path_f
            else:
                continue
        return path_f

def w_check_pem(path_f: str) -> str:
    """Проверяет путь для записи .pem файла.
    Требует расширение .pem; если файл уже существует — спрашивает,
    перезаписывать ли его. Возвращает подтверждённый путь."""
    while True:
        if not path_f.lower().endswith(".pem"):
            path_f = input(f"path {path_f} does not lead to a .pem file. pls rewrite: ")
            continue
        if os.path.isfile(path_f):
            ans = input(f"file {path_f} already exists, do you want to rewrite it?(y/n): ")
            if ans.lower() == 'n':
                path_f = input("then input new path: ")
                continue
            if ans.lower() == 'y':
                return path_f
            else:
                continue
        return path_f

def get_keys_paths() -> list[str]:
    """Запрашивает у пользователя пути для сохранения трёх ключей:
    симметричного (txt), открытого (pem) и закрытого (pem).
    Проверяет пути и гарантирует, что пути pem-ключей различаются.
    Возвращает список из трёх путей."""
    print("input absolute paths for serialization of keys")
    print("if its not absolute path, program will put then into ", os.getcwd(), " directory")
    paths = ["", "", ""]
    paths[0] = input("symmetrical cyphered key: ")
    paths[1] = input("open key: ")
    paths[2] = input("closed key: ")

    print("\nchecking pathways...")
    time.sleep(2)

    paths[0] = w_check_txt(paths[0])
    for idx in range(1, 3):
        paths[idx] = w_check_pem(paths[idx])
    while paths[2] == paths[1]:
        paths[2] = input("pem files have similar paths, pls rewrite second pem file: ")
        w_check_pem(paths[2])

    print(paths)

    print("pathways passed the checks\n")

    return paths

def keys(n: int) -> None:
    """Генерирует ключи для шифрования.
    Создаёт симметричный ключ длиной n бит, пару RSA-ключей,
    шифрует симметричный ключ открытым ключом и сериализует всё
    в файлы (по умолчанию 1.txt, 2.pem, 3.pem или пользовательские)."""
    print("\nright now you want to generate new keys for cyphering")
    paths = ["1.txt","2.pem","3.pem"]
    while True:
        a =  input("would you like key path to be default(1.txt 2.pem 3.pem), existing ones would be rewritten(y,n): ")
        if a.lower() == 'y':
            break
        if a.lower() == 'n':
            paths = get_keys_paths()
            break

    print("\ngenerating symmetrical key...")
    time.sleep(1)
    sym_key = os.urandom(n // 8)

    print("generating open and closed keys...")
    time.sleep(1)
    asym_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024
    )
    private_key = asym_key
    public_key = asym_key.public_key()

    print("\nencrypting symmetrical key...")
    time.sleep(1)

    cipher_sym_key = public_key.encrypt(
        sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("serializing keys...")
    time.sleep(1)

    with open(paths[0], 'wb') as key_file:
        key_file.write(cipher_sym_key)

    with open(paths[1], 'wb') as public_out:
        public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo))

    with open(paths[2], 'wb') as private_out:
        private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                    encryption_algorithm=serialization.NoEncryption()))

    print("process complete")

def get_encrypting_paths() -> list[str]:
    """Запрашивает пути для шифрования файла: исходный текст,
    закрытый ключ, зашифрованный симметричный ключ, выходной файл.
    Проверяет корректность путей и их различие.
    Возвращает список из четырёх путей."""
    paths = ["","","",""]

    print("input absolute paths for encrypting pf the file")
    print("if its not absolute path, program will put then into ", os.getcwd(), " directory")

    paths[0] = input("original text: ")
    paths[1] = input("private key: ")
    paths[2] = input("encrypted symmetrical key: ")
    paths[3] = input("encrypted text: ")

    print("\nchecking paths...")
    time.sleep(1)
    paths[0] = r_check_txt(paths[0])
    paths[1] =  r_check_pem(paths[1])
    while paths[2] == paths[0]:
        paths[2] = input(f"original text and symmetrical key have similar paths, pls rewrite the later: ")
        paths[2] = r_check_txt(paths[2])
    paths[3] = w_check_txt(paths[3])
    print("paths passed the checks")

    return paths

def cypher() -> None:
    """Шифрует текстовый файл.
    Читает зашифрованный симметричный ключ, расшифровывает его
    закрытым ключом, дополняет исходный текст, шифрует AES-CBC
    со случайным IV и сохраняет IV + шифротекст в выходной файл."""
    paths = ["text.txt","3.pem","1.txt","encrypted_text.txt"]
    print("\nright now you want to encrypt txt file")
    while True:
        a = input("do you want to use default file paths?(y/n): ")
        if a.lower() == 'y':
            break
        if a.lower() == 'n':
            paths = get_encrypting_paths()
            break

    print("\nreading symmetrical key...")
    time.sleep(1)
    with open(paths[2],"rb") as sym_key_file:
        encrypted_sym_key = sym_key_file.read()

    print("reading private key...")
    time.sleep(1)
    with open(paths[1], 'rb') as pem_in:
        private_bytes = pem_in.read()
    private_key = serialization.load_pem_private_key(private_bytes, password=None, )

    print("decrypting symmetrical key...")
    time.sleep(1)
    sym_key = private_key.decrypt(encrypted_sym_key,
                                  asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                               label=None))


    print("reading/padding original text...")
    time.sleep(1)
    with open(paths[0],"rb") as original:

        pad = sym_padding.ANSIX923(128).padder()
        #text = bytes(original.read(), 'UTF-8') используеться для 'поддверждения' кодировки текста
        padded_text = pad.update(original.read()) + pad.finalize()

    print("\nencrypting text...")
    time.sleep(1)

    iv = os.urandom(16)  # случайное значение для инициализации блочного режима, должно быть размером с блок и каждый раз новым
    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()

    print("saving encrypted text...")
    time.sleep(1)
    with open(paths[3], "wb") as encrypted:
        encrypted.write(iv)
        encrypted.write(c_text)

    print("process complete")

def get_decrypting_paths() -> list[str]:
    """Запрашивает пути для дешифрования файла: зашифрованный текст,
    закрытый ключ, зашифрованный симметричный ключ, выходной файл.
    Проверяет корректность путей и их различие.
    Возвращает список из четырёх путей."""
    paths = ["","","",""]

    print("input absolute paths for decrypting of the file")
    print("if its not absolute path, program will put then into ", os.getcwd(), " directory")

    paths[0] = input("encrypted text: ")
    paths[1] = input("private key: ")
    paths[2] = input("encrypted symmetrical key: ")
    paths[3] = input("decrypted text: ")

    print("\nchecking paths...")
    time.sleep(1)
    paths[0] = r_check_txt(paths[0])
    paths[1] =  r_check_pem(paths[1])
    while paths[2] == paths[0]:
        paths[2] = input(f"encrypted text and symmetrical key have similar paths, pls rewrite the later: ")
        paths[2] = r_check_txt(paths[2])
    paths[3] = w_check_txt(paths[3])
    print("paths passed the checks")

    return paths

def decypher() -> None:
    """Дешифрует текстовый файл.
    Читает зашифрованный симметричный ключ, расшифровывает его
    закрытым ключом, извлекает IV, дешифрует AES-CBC,
    снимает дополнение ANSIX923 и сохраняет исходный текст."""
    paths = ["encrypted_text.txt","3.pem","1.txt","decrypted_text.txt"]
    print("\nright now you want to decrypt txt file")
    while True:
        a = input("do you want to use default file paths?(y/n): ")
        if a.lower() == 'y':
            break
        if a.lower() == 'n':
            paths = get_decrypting_paths()
            break


    print("\nreading symmetrical key...")
    time.sleep(1)
    with open(paths[2],"rb") as sym_key_file:
        encrypted_sym_key = sym_key_file.read()

    print("reading private key...")
    time.sleep(1)
    with open(paths[1], 'rb') as pem_in:
        private_bytes = pem_in.read()
    private_key = serialization.load_pem_private_key(private_bytes, password=None, )

    print("decrypting symmetrical key...")
    time.sleep(1)
    sym_key = private_key.decrypt(encrypted_sym_key,
                                  asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                                                    algorithm=hashes.SHA256(),
                                                    label=None))

    print("reading encrypted text...")
    time.sleep(1)
    with open(paths[0], "rb") as encrypted:
        encrypted_text = encrypted.read()

    iv = encrypted_text[:16]
    encrypted_text = encrypted_text[16:]

    print("\ndecrypting text...")
    time.sleep(1)

    cipher = Cipher(algorithms.AES(sym_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(encrypted_text) + decryptor.finalize()

    unpadder = sym_padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    print("saving decrypted text...")
    time.sleep(1)
    with open(paths[3], "wb") as decrypted:
        decrypted.write(unpadded_dc_text)



def main():

    n = 128

    while True:

        print("\nthis program is used for hybrid of symmetrical and asymmetrical cyphering")
        print("here you can generate keys(1), cypher your txt files(2) and decypher them(3), change key length(4), exit(0)")
        a = input("what do you want do now: ")
        if a == '0':
            break
        if a == '1':
            keys(n)
        if a == '2':
            cypher()
        if a == '3':
            decypher()
        if a == '4':
            print(f'\ncurrently key size equals {n}')
            n_p = input("input 128, 192 or 256 for length of key: ")
            if n_p.isdigit() and int(n_p) in [128,192,256]:
                    n = int(n_p)
            else:
                print(f'{n_p} is not one of allowed length for keys')
        else:
            continue

if __name__ == '__main__':
    main()

