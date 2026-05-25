"""
Главный файл запуска проекта.
"""

import sys


def main() -> None:
    """
    Определяет режим запуска программы.
    """

    if len(sys.argv) > 1:
        from cli_interface import start_cli

        start_cli()

    else:
        try:
            from gui_pyqt import run_interface

            run_interface()

        except ImportError:
            from backup_gui import BackupWindow

            app = BackupWindow()
            app.run()


if __name__ == "__main__":
    main()
