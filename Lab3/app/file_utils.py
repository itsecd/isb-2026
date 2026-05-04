# работа с файлами (DRY)

def write_bytes(path: str, data: bytes):
    if not path:
        raise ValueError("Путь к файлу не задан")

    with open(path, "wb") as f:
        f.write(data)


def read_bytes(path: str) -> bytes:
    if not path:
        raise ValueError("Путь к файлу не задан")

    with open(path, "rb") as f:
        return f.read()


def write_text(path: str, data: str):
    if not path:
        raise ValueError("Путь к файлу не задан")

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def read_text(path: str) -> str:
    if not path:
        raise ValueError("Путь к файлу не задан")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()