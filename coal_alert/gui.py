import sys
import math
import collisions

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QTextEdit, QProgressBar, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPixmap


class ExperimentWorker(QThread):
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, bits_list, experiments, str_len):
        super().__init__()
        self.bits_list = bits_list
        self.experiments = experiments
        self.str_len = str_len

    def run(self):
        try:
            results = {}
            total_steps = len(self.bits_list) * self.experiments
            current_step = 0

            for bits in self.bits_list:
                total_attempts = 0
                example_collision = None
                
                for i in range(self.experiments):
                    if self.isInterruptionRequested():
                        return
                    
                    res = collisions.find_collision(bits, self.str_len)
                    if res:
                        s1, s2, h, attempts = res
                        total_attempts += attempts
                        if example_collision is None:
                            example_collision = (s1, s2, h)
                    
                    current_step += 1
                    progress_percent = int((current_step / total_steps) * 100)
                    self.progress_signal.emit(progress_percent, f"Тестирование {bits} бит... Шаг {i+1}/{self.experiments}")
                
                avg_attempts = total_attempts / self.experiments
                theoretical = math.sqrt(math.pi * (2 ** bits) / 2)
                
                results[bits] = {
                    "avg_practice": avg_attempts,
                    "theory": theoretical,
                    "example": example_collision
                }
            
            self.finished_signal.emit(results)
        except Exception as e:
            self.error_signal.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COAL")
        self.setMinimumSize(1000, 1000)
        
        self.background_pixmap = QPixmap("CobsonStardust.png")
        
        self.init_ui()

    def paintEvent(self, event):
        """
        Отрисовка фонового изображения на весь холст окна при перерисовках.
        """
        painter = QPainter(self)
        if not self.background_pixmap.isNull():
            painter.drawPixmap(self.rect(), self.background_pixmap)
        else:
            super().paintEvent(event)

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("central_container")
        layout = QVBoxLayout(central_widget)

        config_layout = QHBoxLayout()
        
        lbl_exp = QLabel("Экспериментов (гемчиков):")
        config_layout.addWidget(lbl_exp)
        self.spin_experiments = QSpinBox()
        self.spin_experiments.setRange(1, 10000)
        self.spin_experiments.setValue(1000)
        config_layout.addWidget(self.spin_experiments)

        lbl_len = QLabel("Длина строк:")
        config_layout.addWidget(lbl_len)
        self.spin_strlen = QSpinBox()
        self.spin_strlen.setRange(4, 64)
        self.spin_strlen.setValue(16)
        config_layout.addWidget(self.spin_strlen)

        layout.addLayout(config_layout)

        self.btn_start = QPushButton("Сделать красиво")
        self.btn_start.clicked.connect(self.start_experiments)
        layout.addWidget(self.btn_start)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.lbl_status = QLabel("Готов к старту")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_status)

        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)

        self.txt_output.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                font-size: 30pt;
            }""")

        layout.addWidget(self.txt_output)

        self.setCentralWidget(central_widget)

    def start_experiments(self):
        self.btn_start.setEnabled(False)
        self.txt_output.clear()
        self.progress_bar.setValue(0)
        
        bits_list = [8, 12, 16]
        experiments = self.spin_experiments.value()
        str_len = self.spin_strlen.value()

        self.worker = ExperimentWorker(bits_list, experiments, str_len)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.display_results)
        self.worker.error_signal.connect(self.handle_error)
        self.worker.start()

    def update_progress(self, value, text):
        self.progress_bar.setValue(value)
        self.lbl_status.setText(text)

    def display_results(self, results):
        self.btn_start.setEnabled(True)
        self.lbl_status.setText("Вычисления успешно завершены!")
        
        out = []
        out.append("-= GEM ALERT =-")
        for bits, data in results.items():
            out.append(f"\n• Результаты для {bits} бит:")
            out.append(f"  Практическое среднее число попыток: {data['avg_practice']:.2f}")
            out.append(f"  Теоретическое число попыток: {data['theory']:.2f}")
        
        self.txt_output.setText("\n".join(out))

    def handle_error(self, e):
        self.btn_start.setEnabled(True)
        self.lbl_status.setText("Произошла ошибка.")
        QMessageBox.critical(self, "Критическое исключение", f"Произошел сбой: {e}")

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())