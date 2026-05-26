"""
Simple PyQt6 GUI for file hashing and integrity verification.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QTextEdit,
    QMessageBox,
)

from hash_utils import sha256_file, save_checksum, verify_file, write_verification_result


class MainWindow(QMainWindow):
    """
    Main window of the file integrity checker GUI.
    """

    def __init__(self):
        """
        Initialize the window and interface controls.
        """
        super().__init__()
        self.setWindowTitle("File Integrity Checker")
        self.file_path = None

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        self.label = QLabel("No file selected")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        btn_select = QPushButton("Select file")
        btn_hash = QPushButton("Compute hash")
        btn_save = QPushButton("Save checksum")
        btn_verify = QPushButton("Verify integrity")

        btn_select.clicked.connect(self.select_file)
        btn_hash.clicked.connect(self.compute_hash)
        btn_save.clicked.connect(self.save_hash)
        btn_verify.clicked.connect(self.verify)

        layout.addWidget(self.label)
        layout.addWidget(btn_select)
        layout.addWidget(btn_hash)
        layout.addWidget(btn_save)
        layout.addWidget(btn_verify)
        layout.addWidget(self.output)

    def select_file(self):
        """
        Open a file picker dialog and store selected path.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Select file")
        if path:
            self.file_path = path
            self.label.setText(path)

    def compute_hash(self):
        """
        Compute and display the SHA-256 hash of the selected file.
        """
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Select a file first")
            return
        try:
            h = sha256_file(self.file_path)
            self.output.setPlainText(h)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_hash(self):
        """
        Save the checksum of the selected file.
        """
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Select a file first")
            return
        try:
            h = sha256_file(self.file_path)
            out = save_checksum(self.file_path, h)
            self.output.setPlainText(f"Saved: {out}\n{h}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def verify(self):
        """
        Verify the selected file and write verification result to a file.
        """
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Select a file first")
            return
        try:
            ok, current, saved = verify_file(self.file_path)
            result = write_verification_result(ok, current, saved)
            self.output.setPlainText(
                f"Current: {current}\nSaved: {saved}\n{'OK' if ok else 'FAILED'}\n{result}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


def main():
    """
    Launch the Qt application.
    """
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()