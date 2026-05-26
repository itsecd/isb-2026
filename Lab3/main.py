
import json
import tkinter as tk

from app.gui import App


def load_settings(path: str = "settings.json") -> dict:
    """
    Загружает настройки из JSON-файла.

    :param path: путь к JSON-файлу настроек
    :return: словарь настроек
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Файл настроек {path} не найден")
        raise

    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON-файла {path}")
        raise

    except Exception as error:
        print(f"Ошибка при чтении настроек: {error}")
        raise

def load_const(path: str = "const.json") -> dict:
    """
    Загружает const.json.

    :param path: путь к JSON-файлу констант
    :return: словарь констант
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Файл констант {path} не найден")
        raise

    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON-файла {path}")
        raise

    except Exception as error:
        print(f"Ошибка при чтении констант: {error}")
        raise

def run_gui(settings: dict) -> None:
    """
    Запускает графический интерфейс приложения.

    :param settings: словарь настроек
    """
    try:
        root = tk.Tk()
        App(root, settings)
        root.mainloop()

    except Exception as error:
        print(f"Ошибка запуска GUI: {error}")
        raise


def main() -> None:
    """
    Точка входа приложения.
    """
    try:
        settings = load_settings()
        run_gui(settings)

    except Exception as error:
        print(f"Ошибка выполнения программы: {error}")


if __name__ == "__main__":
    main()
