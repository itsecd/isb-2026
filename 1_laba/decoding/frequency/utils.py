def read(path_input: str) -> str:
    """Считывание файла"""
    with open(path_input, 'r', encoding="utf-8") as f:
        text = f.read()

    return text

def write(path_output: str, encoding_text: str) -> None:
    """Запись в файл"""
    with open(path_output, 'w', encoding="utf-8") as f:
        f.write(encoding_text)