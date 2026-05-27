import sys
from PyQt5.QtWidgets import QApplication

# Импортируем наш класс интерфейса из модуля app.py
from app import CryptoApp

def main():
    """
    Главная точка входа в приложение гибридной криптосистемы.
    Инициализирует окружение Qt и запускает главный цикл обработки событий.
    """
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    
    # sys.exit обеспечивает чистое завершение процесса при закрытии окна
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()