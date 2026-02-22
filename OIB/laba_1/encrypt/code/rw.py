def read(path_original: str) -> str:
    with open(path_original, 'r', encoding="utf-8") as f:
        text = f.read()

    return text

def write(path_encrypted: str, encoding_text: str) -> None:
    with open(path_encrypted, 'w', encoding="utf-8") as f:
        f.write(encoding_text) 