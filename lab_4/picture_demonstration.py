from PIL import Image, UnidentifiedImageError
from file_open_and_close import load_config

def show_picture(config_path: str):
    """
    Загружает конфигурацию и открывает картинку с помощью стандартного просмотрщика.
    Args:
        config_path (str): Путь к файлу конфигурации (например, 'settings.json').
    Returns:
        None: Функция ничего не возвращает, только выполняет действие (показ картинки).
    """
    config = load_config(config_path)
    picture_path = config.get("files", {}).get("cat_picture", "cat.jpg")
    try:
        image = Image.open(picture_path)
        image.show()
        print("Enjoy your cat")
    except FileNotFoundError:
        print(f"Error: Picture '{picture_path}' not found.")
    except UnidentifiedImageError:
        print(f"Error: '{picture_path}' is corrupted or not a valid image.")
