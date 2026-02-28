import os


def read_bitstring(path: str, expected_len: int = 128) -> str:
    """Читает бинарную строку 0/1 из файла и проверяет длину."""
    with open(path, "r", encoding="utf-8") as f:
        raw: str = f.read().strip()
    seq: str = "".join(ch for ch in raw if ch in "01")
    if len(seq) != expected_len:
        raise ValueError(f"Ожидается {expected_len} бит, получено {len(seq)} бит.")
    return seq


def ensure_dir(dir_path: str) -> None:
    """Создаёт папку для сохранения результатов."""
    os.makedirs(dir_path, exist_ok=True)


def write_text(path: str, text: str) -> None:
    """Записывает текст в файл."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)