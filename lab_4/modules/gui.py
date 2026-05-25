# -*- coding: utf-8 -*-
"""PyQt6 graphical user interface for HMACTask.

Provides four tabs:
    1. Generate – compute and save a signed envelope.
    2. Verify   – load an envelope and verify its HMAC.
    3. Tamper   – check that a modified message is rejected.
    4. Collision – visual partial-collision search (runs in a QThread).
"""

import json
import threading
from pathlib import Path

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import modules.hmac_core as hmac_core
import modules.collision as collision
import modules.logger as logger

log = logger.app_logger


# ---------------------------------------------------------------------------
# Worker thread for collision search
# ---------------------------------------------------------------------------

class CollisionWorker(QThread):
    """Background thread that runs the partial-collision search.

    Signals:
        result (str): Emitted with a human-readable result string when done.
        progress (int): Emitted periodically with the attempt count (unused
            directly; tqdm handles terminal output).
    """

    result = pyqtSignal(str)

    def __init__(self, secret_key: str, prefix_bits: int, parent=None) -> None:
        super().__init__(parent)
        self._secret_key = secret_key
        self._prefix_bits = prefix_bits

    def run(self) -> None:
        """Execute the collision search and emit :attr:`result`."""
        found = collision.find_partial_collision(self._secret_key, self._prefix_bits)
        if found:
            msg_a, msg_b, prefix = found
            text = (
                f"Collision found!\n\n"
                f"Message A : {msg_a}\n"
                f"Message B : {msg_b}\n"
                f"Shared prefix : {prefix}"
            )
        else:
            text = "No collision found within the attempt limit."
        self.result.emit(text)


# ---------------------------------------------------------------------------
# Individual tab widgets
# ---------------------------------------------------------------------------

class _GenerateTab(QWidget):
    """Tab for computing and saving a signed HMAC envelope."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # --- Inputs ---
        grp = QGroupBox("Input")
        grp_layout = QVBoxLayout(grp)

        grp_layout.addWidget(QLabel("Secret key:"))
        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit.setPlaceholderText("Enter shared secret key…")
        grp_layout.addWidget(self.key_edit)

        grp_layout.addWidget(QLabel("Message:"))
        self.msg_edit = QTextEdit()
        self.msg_edit.setPlaceholderText("Type your message here…")
        self.msg_edit.setMaximumHeight(100)
        grp_layout.addWidget(self.msg_edit)

        grp_layout.addWidget(QLabel("Output file:"))
        file_row = QHBoxLayout()
        self.file_edit = QLineEdit("signed.json")
        file_row.addWidget(self.file_edit)
        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._browse)
        file_row.addWidget(browse_btn)
        grp_layout.addLayout(file_row)

        layout.addWidget(grp)

        # --- Action ---
        sign_btn = QPushButton("Sign & Save")
        sign_btn.clicked.connect(self._sign)
        layout.addWidget(sign_btn)

        # --- Result ---
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setFont(QFont("Courier New", 9))
        layout.addWidget(self.result_edit)

    def _browse(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save signed envelope", "", "JSON Files (*.json)"
        )
        if path:
            self.file_edit.setText(path)

    def _sign(self) -> None:
        key = self.key_edit.text().strip()
        msg = self.msg_edit.toPlainText().strip()
        path = self.file_edit.text().strip()

        if not key or not msg:
            QMessageBox.warning(self, "Input error", "Key and message are required.")
            return

        try:
            envelope = hmac_core.sign_and_save(msg, key, path)
            self.result_edit.setPlainText(json.dumps(envelope, indent=2))
        except Exception as exc:
            log.error("Sign error: %s", exc)
            QMessageBox.critical(self, "Error", str(exc))


class _VerifyTab(QWidget):
    """Tab for loading and verifying a signed envelope."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        grp = QGroupBox("Input")
        grp_layout = QVBoxLayout(grp)

        grp_layout.addWidget(QLabel("Secret key:"))
        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        grp_layout.addWidget(self.key_edit)

        grp_layout.addWidget(QLabel("Envelope file:"))
        file_row = QHBoxLayout()
        self.file_edit = QLineEdit("signed.json")
        file_row.addWidget(self.file_edit)
        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._browse)
        file_row.addWidget(browse_btn)
        grp_layout.addLayout(file_row)

        layout.addWidget(grp)

        verify_btn = QPushButton("Verify")
        verify_btn.clicked.connect(self._verify)
        layout.addWidget(verify_btn)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(self.status_label)

        self.detail_edit = QTextEdit()
        self.detail_edit.setReadOnly(True)
        self.detail_edit.setFont(QFont("Courier New", 9))
        layout.addWidget(self.detail_edit)

    def _browse(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open envelope", "", "JSON Files (*.json)"
        )
        if path:
            self.file_edit.setText(path)

    def _verify(self) -> None:
        key = self.key_edit.text().strip()
        path = self.file_edit.text().strip()

        if not key:
            QMessageBox.warning(self, "Input error", "Secret key is required.")
            return

        try:
            is_valid, envelope = hmac_core.load_and_verify(path, key)
            color = "#27ae60" if is_valid else "#e74c3c"
            text = "✓  VALID" if is_valid else "✗  INVALID"
            self.status_label.setText(text)
            self.status_label.setStyleSheet(f"color: {color};")
            self.detail_edit.setPlainText(json.dumps(envelope, indent=2))
        except Exception as exc:
            log.error("Verify error: %s", exc)
            QMessageBox.critical(self, "Error", str(exc))


class _TamperTab(QWidget):
    """Tab for demonstrating tamper detection."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        grp = QGroupBox("Input")
        grp_layout = QVBoxLayout(grp)

        grp_layout.addWidget(QLabel("Secret key:"))
        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        grp_layout.addWidget(self.key_edit)

        grp_layout.addWidget(QLabel("Original envelope file:"))
        file_row = QHBoxLayout()
        self.file_edit = QLineEdit("signed.json")
        file_row.addWidget(self.file_edit)
        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._browse)
        file_row.addWidget(browse_btn)
        grp_layout.addLayout(file_row)

        grp_layout.addWidget(QLabel("Tampered message:"))
        self.tamper_edit = QTextEdit()
        self.tamper_edit.setPlaceholderText("Modify the original message here…")
        self.tamper_edit.setMaximumHeight(80)
        grp_layout.addWidget(self.tamper_edit)

        layout.addWidget(grp)

        check_btn = QPushButton("Check Tampered Message")
        check_btn.clicked.connect(self._check)
        layout.addWidget(check_btn)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        layout.addWidget(self.result_label)

        layout.addStretch()

    def _browse(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open envelope", "", "JSON Files (*.json)"
        )
        if path:
            self.file_edit.setText(path)

    def _check(self) -> None:
        key = self.key_edit.text().strip()
        path = self.file_edit.text().strip()
        tampered = self.tamper_edit.toPlainText().strip()

        if not key or not tampered:
            QMessageBox.warning(self, "Input error", "All fields are required.")
            return

        try:
            result = hmac_core.tamper_and_verify(path, key, tampered)
            if result:
                self.result_label.setText("⚠  ACCEPTED (unexpected!)")
                self.result_label.setStyleSheet("color: #e67e22;")
            else:
                self.result_label.setText("✓  Tampering detected — message rejected")
                self.result_label.setStyleSheet("color: #27ae60;")
        except Exception as exc:
            log.error("Tamper check error: %s", exc)
            QMessageBox.critical(self, "Error", str(exc))


class _CollisionTab(QWidget):
    """Tab for running the partial-collision search with a progress indicator."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        grp = QGroupBox("Parameters")
        grp_layout = QVBoxLayout(grp)

        grp_layout.addWidget(QLabel("Secret key:"))
        self.key_edit = QLineEdit("demo_key")
        grp_layout.addWidget(self.key_edit)

        bits_row = QHBoxLayout()
        bits_row.addWidget(QLabel("Prefix bits (8–32):"))
        self.bits_spin = QSpinBox()
        self.bits_spin.setRange(8, 32)
        self.bits_spin.setValue(20)
        bits_row.addWidget(self.bits_spin)
        bits_row.addStretch()
        grp_layout.addLayout(bits_row)

        layout.addWidget(grp)

        self.run_btn = QPushButton("Run Collision Search")
        self.run_btn.clicked.connect(self._run)
        layout.addWidget(self.run_btn)

        self.info_label = QLabel("Progress is shown in the terminal via tqdm.")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setFont(QFont("Courier New", 9))
        layout.addWidget(self.result_edit)

        self._worker: CollisionWorker | None = None

    def _run(self) -> None:
        key = self.key_edit.text().strip()
        bits = self.bits_spin.value()

        if not key:
            QMessageBox.warning(self, "Input error", "Secret key is required.")
            return

        self.run_btn.setEnabled(False)
        self.result_edit.setPlainText("Searching… (see terminal for tqdm progress)")

        self._worker = CollisionWorker(key, bits)
        self._worker.result.connect(self._on_result)
        self._worker.start()

    def _on_result(self, text: str) -> None:
        self.result_edit.setPlainText(text)
        self.run_btn.setEnabled(True)


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    """Application main window with tab-based navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("HMACTask — Lab 4")
        self.resize(720, 560)

        tabs = QTabWidget()
        tabs.addTab(_GenerateTab(), "🔑  Generate")
        tabs.addTab(_VerifyTab(),   "✅  Verify")
        tabs.addTab(_TamperTab(),   "🔍  Tamper")
        tabs.addTab(_CollisionTab(), "💥  Collision")

        self.setCentralWidget(tabs)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("HMACTask ready")


def run_gui() -> None:
    """Launch the PyQt6 application.

    Creates a :class:`QApplication`, shows the :class:`MainWindow`,
    and starts the event loop.
    """
    import sys

    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
