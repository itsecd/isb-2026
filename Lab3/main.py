import json
import tkinter as tk

from app.gui import App

def load_settings() -> dict:
    """
    Чтение настроек
    """
    with open("settings.json", "r", encoding="utf-8") as f:
        return json.load(f)


def run_gui(settings: dict) -> None:
    """
    Запуск графического интерфейса
    """
    root = tk.Tk()
    App(root, settings)
    root.mainloop()


def main() -> None:
    """
    Точка входа приложения
    """
    settings = load_settings()

    mode = "gui"

    match mode:
        case "gui":
            run_gui(settings)
        case _:
            print("Неизвестный режим запуска")


if __name__ == "__main__":
    main()