"""Точка входа: выбор режима работы."""
import sys

def main():
    # Если есть аргументы командной строки, то CLI режим
    if len(sys.argv) > 1:
        from cli import run_cli
        run_cli()
    else:
        # Иначе GUI на tkinter (не требует PyQt5)
        from gui_tkinter import run_gui
        run_gui()


if __name__ == "__main__":
    main()