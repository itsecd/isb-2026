"""Главный запускной файл гибридной криптосистемы. Запускает графический интерфейс приложения."""

import tkinter as tk
from gui_app import CryptoApp


def main() -> None:
    """Инициализирует графическое окно Tkinter и запускает цикл событий."""
    root = tk.Tk()
    CryptoApp(root, config_path='settings.json')
    root.mainloop()


if __name__ == '__main__':
    main()
