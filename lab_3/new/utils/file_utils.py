import os


def read_bytes(path: str) -> bytes:
    try:
        with open(path, "rb") as f:
            return f.read()

    except FileNotFoundError:
        raise FileNotFoundError(f"[FILE ERROR] Файл не найден: {path}")

    except PermissionError:
        raise PermissionError(f"[FILE ERROR] Нет доступа к файлу: {path}")

    except Exception as e:
        raise RuntimeError(f"[FILE ERROR] Ошибка чтения {path}: {e}")


def write_bytes(path: str, data: bytes) -> None:
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(path, "wb") as f:
            f.write(data)

    except PermissionError:
        raise PermissionError(f"[FILE ERROR] Нет прав на запись: {path}")

    except Exception as e:
        raise RuntimeError(f"[FILE ERROR] Ошибка записи {path}: {e}")
