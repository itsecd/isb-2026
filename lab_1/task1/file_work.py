def read_file(path: str) -> str:
    """Данная функция читает содержимое файла"""
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def write_file(path: str, enctypted_text: str) -> None:
    """Данная функция выполняет запись текста в файл"""
    with open(path, "w", encoding="utf-8") as file:
        file.write(enctypted_text)