
import json
import tkinter as tk

from app.gui import App


def load_json(path: str) -> dict:
    """
    Загружает данные из JSON-файла.

    :param path: путь к JSON-файлу
    :return: словарь с данными
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Файл {path} не найден")
        raise

    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON-файла {path}")
        raise

    except Exception as error:
        print(f"Ошибка при чтении файла: {error}")
        raise

def run_gui(settings: dict, constants: dict) -> None:
    """
    Запускает графический интерфейс приложения.

    :param settings: словарь настроек
    :param constants: словарь констант
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
        settings = load_json("settings.json")
        constants = load_json("const.json")
        run_gui(settings, constants)

    except Exception as error:
        print(f"Ошибка выполнения программы: {error}")


if __name__ == "__main__":
    main()
