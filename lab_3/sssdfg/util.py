import json
from cryptography.hazmat.primitives import serialization

def read_file(filepath: str) -> bytes:
    """
    Считывает и возвращает байты из файла
    Принимает:
        filepath - путь к файлу
    Возвращает:
        - считанные байты.
    """
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {filepath}, увы")

def read_json_file(filepath: str) -> dict:
    """
    Чтение .json файла по указанному пути в словарь.
    Принимает:
        filepath - путь до .json файла.
    Возвращает:
        - словарь со считанными из файла данными
    """
    try:
        with open(filepath, 'r') as fp:
            json_data = json.load(fp)
        return json_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось открыть файл {filepath}, увы")
    

def write_public_key(public_pem: str, public_key: bytes,) -> None:
    """
    Функция для записей ключей асимметричного алгоритма в указанные файлы
    Принимает:
        public_pem - путь для сохранения открытого ключа
        public_key - открытый ключ
    """
    try:
        with open(public_pem, 'wb') as public_out:
                    public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo))
    except Exception as e:
        print("Увынск Топор+ подписаться:", e) 

def write_private_key(private_pem: str, private_key: bytes) -> None:
    """
    Функция для записей ключей асимметричного алгоритма в указанные файлы
    Принимает:
        private_pem - путь для сохранения закрытого ключа
        private_key - закрытый ключ
    """
    try:
        with open(private_pem, 'wb') as private_out:
                    private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()))
    except Exception as e:
        print("Увынск Топор+ подписаться:", e) 


def write_file(filepath: str, text: str) -> None:
      """
      Функция для записи данных в файл
      Принимает:
        filepath - путь до файла для записи
        text - данные для записи
      """
    try:
      with open (filepath, "wb") as f:
            f.write(text)
    except Exception as e:
        print("Увынск Топор+ подписаться:", e) 
