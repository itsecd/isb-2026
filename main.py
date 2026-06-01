import sys
from PyQt5.QtWidgets import QApplication
from py_qt import Hash_app


def main() -> None:
    """
    Инициализирует Qt-приложение и запускает главное окно графического интерфейса.
    """
    app = QApplication(sys.argv)
    window = Hash_app()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
