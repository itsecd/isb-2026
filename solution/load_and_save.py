def read_data(data_path:str) -> str:
    """
    Чтение данных из файла
    Входные данные:
    data_path - путь к файлу с данными
    Возвращает:
    Считанные данные(str)
    """
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def write_data(data: str,  file_path: str) -> None:
    """
    Запись данных в файл
    Входные данные:
    data - данные
    file_path - путь к сохранению файла
    Возвращает:
    None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception:
        return
