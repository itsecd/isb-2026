import os
import sys

from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton,
QTextEdit, QVBoxLayout, QWidget)
from work_with_hash import (calculate_hash, write_hash, hash_comparison, clear_hash_file, find_part_collision)


class IntegrityCheckerWindow(QMainWindow):

    def __init__(self):
        """ настраивает главное окно """

        super().__init__()

        self.setWindowTitle("Проверка целостности файлов с использованием хеш-функций")
        self.resize(650, 450)

        self.selected_file_path = ""
        self.hash_storage_file = "calculated_hash.txt"

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        file_layout = QHBoxLayout()
        self.file_label = QLabel("Выберите файл")
        self.file_label.setStyleSheet("font-weight: bold; color: #000;")
        btn_select = QPushButton("Выбрать файл")
        btn_select.clicked.connect(self.browse_file)
        file_layout.addWidget(btn_select)
        file_layout.addWidget(self.file_label, stretch=1)
        main_layout.addLayout(file_layout)

        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("Количество символов хеша, которые будут совпадать, для нахождения коллизии (1-5):"))
        self.prefix_input = QLineEdit("4")
        self.prefix_input.setFixedWidth(50)
        prefix_layout.addWidget(self.prefix_input)
        prefix_layout.addStretch()
        main_layout.addLayout(prefix_layout)

        buttons_layout = QHBoxLayout()
        self.btn_save = QPushButton("1. Сохранить хеш")
        self.btn_check = QPushButton("2. Проверить целостность")
        self.btn_collision = QPushButton("3. Подобрать коллизию")
        self.btn_clear = QPushButton("Очистить сохраненный хеш")

        self.btn_save.clicked.connect(self.action_save_hash)
        self.btn_check.clicked.connect(self.action_check_integrity)
        self.btn_collision.clicked.connect(self.action_find_collision)
        self.btn_clear.clicked.connect(self.action_clear_hash)

        self.btn_save.setEnabled(False)
        self.btn_check.setEnabled(False)
        self.btn_collision.setEnabled(False)

        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_check)
        buttons_layout.addWidget(self.btn_collision)
        buttons_layout.addWidget(self.btn_clear)
        main_layout.addLayout(buttons_layout)

        main_layout.addWidget(QLabel("Действия:"))
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #f8f9fa; font-family: Courier;")
        main_layout.addWidget(self.log_area)


    def browse_file(self):
        """открывает диалоговое окно для выбора файла"""

        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            self.file_label.setText(file_name)

            self.btn_save.setEnabled(True)
            self.btn_check.setEnabled(True)
            self.btn_collision.setEnabled(True)

            self.log_area.append(f"Выбран файл: {file_path}")


    def action_save_hash(self):
        """логика кнопки создания эталонного хеша"""

        try:
            current_hash = calculate_hash(self.selected_file_path)
            write_hash(self.hash_storage_file, current_hash)

            self.log_area.append(f"\nХеш сохранен в '{self.hash_storage_file}'")
            self.log_area.append(f"Хеш: {current_hash}")

            QMessageBox.information(self, "Успех", "Хеш успешно сохранен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать хеш: {e}")


    def action_check_integrity(self):
        """логика кнопки проверки целостности"""

        if not os.path.exists(self.hash_storage_file):
            QMessageBox.warning(self,"Проблема","Файл с эталонным хешем не найден.\nСначала создайте эталонный хеш и сохраните его.")
            return

        try:
            check_result = hash_comparison(self.selected_file_path, self.hash_storage_file)

            self.log_area.append("\nПроверка целостности")
            self.log_area.append(f"Эталонный хеш: {check_result['hash from file']}")
            self.log_area.append(f"Текущий хеш:   {check_result['calculated hash']}")

            if check_result["comparison"]:
                self.log_area.append("Файл прошёл проверку целостности.")
                QMessageBox.information(self,"Результат проверки","Файл прошёл проверку целостности, изменения не обнаружены.")
            else:
                self.log_area.append("Файл был изменён, целостность нарушена.")
                QMessageBox.critical(self,"Результат проверки","Файл не прошёл проверку целостности, в него внесены изменения.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка проверки: {e}")


    def action_find_collision(self):
        """Логика кнопки подбора частичной коллизии"""

        self.log_area.append(f"\nЗапуск подбора коллизии для файла: {os.path.basename(self.selected_file_path)}")
        self.log_area.append("Смотрите полосу загрузки tqdm в терминале...")

        QApplication.processEvents()

        try:
            prefix_len = int(self.prefix_input.text())
        except ValueError:
            QMessageBox.critical(self, "Ошибка ввода", "Количество символов должно быть числом!")
            return

        result = find_part_collision(
            self.selected_file_path, part_len=prefix_len
        )

        self.log_area.append("\nСодержимое словаря result:")
        for key, value in result.items():
            self.log_area.append(f"{key}: {value}")

        if "error" in result:
            QMessageBox.critical(self, "Ошибка подбора", result["error"])
        elif result.get("collision"):
            QMessageBox.information(self,"Успех подбора",f"Частичная коллизия найдена за {result['number of steps']} шагов.\n\nСтрока: {result['string']}")
        else:
            QMessageBox.warning(self, "Неудача", "За отведенное число шагов частичная коллизия не найдена.")

    def action_clear_hash(self):
        """логика новой кнопки для удаления файла хеша с диска"""

        if os.path.exists(self.hash_storage_file):
            clear_hash_file(self.hash_storage_file)
            self.log_area.append(f"\nФайл '{self.hash_storage_file}' успешно удален с диска.")
            QMessageBox.information(self, "Успех", "Файл с сохраненным хешем успешно удален.")
        else:
            self.log_area.append("\nПопытка очистки: сохраненного хеша и так не существовало.")
            QMessageBox.warning(self,"Внимание","Файл с эталонным хешем уже пуст или не создан.")


def main():
    app = QApplication(sys.argv)
    window = IntegrityCheckerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()