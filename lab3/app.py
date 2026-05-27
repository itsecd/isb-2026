import argparse
import sys
from datetime import datetime

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton,
    QSlider, QVBoxLayout, QWidget, QFrame,
)

from config import (
    CAST5_MIN_BITS,
    CAST5_MAX_BITS,
)

from rsa_utils import (
    generate_rsa_keys,
    encrypt_symmetric_key,
    decrypt_symmetric_key,
)

from cast5_utils import (
    generate_cast5_key,
    encrypt_file,
    decrypt_file,
)

from cli import (
    keygen_mode,
    encrypt_mode,
    decrypt_mode,
)
from file_utils import load_settings, save_settings, get_file_size_str


class WorkerThread(QThread):
    log_signal      = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    done_signal     = pyqtSignal(bool, str)

    def __init__(self, task_fn):
        super().__init__()
        self._task_fn = task_fn

    def run(self):
        try:
            self._task_fn(self.log_signal, self.progress_signal)
            self.done_signal.emit(True, "")
        except Exception as exc:
            self.done_signal.emit(False, str(exc))


class PathField(QWidget):
    def __init__(self, placeholder="", file_filter="All files (*)", save_mode=False):
        super().__init__()
        self._file_filter = file_filter
        self._save_mode   = save_mode

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)

        self.edit = QLineEdit()
        self.edit.setPlaceholderText(placeholder)

        self.btn = QPushButton("…")
        self.btn.setFixedSize(30, 30)
        self.btn.setObjectName("browseBtn")
        self.btn.clicked.connect(self._browse)

        lay.addWidget(self.edit)
        lay.addWidget(self.btn)

    def _browse(self):
        fn = QFileDialog.getSaveFileName if self._save_mode else QFileDialog.getOpenFileName
        path, _ = fn(self, "", "", self._file_filter)
        if path:
            self.edit.setText(path)

    def text(self):       return self.edit.text().strip()
    def setText(self, t): self.edit.setText(t)


class CryptoApp(QWidget):
    def __init__(self, initial_settings=None):
        super().__init__()
        self.settings     = initial_settings or {}
        self._worker      = None
        self._valid_sizes = list(range(CAST5_MIN_BITS, CAST5_MAX_BITS + 1, 8))

        self.setWindowTitle("RSA + CAST5  //  Криптосистема")
        self.setMinimumSize(860, 660)

        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        self._apply_styles()

        if self.settings:
            self._apply_settings(self.settings)

    def _create_widgets(self):
        self.btn_keygen  = QPushButton("Сгенерировать ключи")
        self.btn_encrypt = QPushButton("Зашифровать файл")
        self.btn_decrypt = QPushButton("Расшифровать файл")
        for b in (self.btn_keygen, self.btn_encrypt, self.btn_decrypt):
            b.setFixedHeight(46)
            b.setObjectName("mainBtn")

        self.cfg_path = PathField("settings.json", "JSON (*.json)")
        self.load_btn = QPushButton("Загрузить")
        self.save_btn = QPushButton("Сохранить")
        for b in (self.load_btn, self.save_btn):
            b.setObjectName("cfgBtn")
            b.setFixedHeight(30)

        self.input_path    = PathField("не задан")
        self.enc_out_path  = PathField("не задан", "Binary (*.bin);;All (*)", save_mode=True)
        self.dec_out_path  = PathField("не задан", save_mode=True)
        self.enc_key_path  = PathField("не задан", "Key (*.enc);;All (*)", save_mode=True)
        self.pub_key_path  = PathField("не задан", "PEM (*.pem);;All (*)", save_mode=True)
        self.priv_key_path = PathField("не задан", "PEM (*.pem);;All (*)", save_mode=True)

        self.key_slider = QSlider(Qt.Horizontal)
        self.key_slider.setMinimum(0)
        self.key_slider.setMaximum(len(self._valid_sizes) - 1)
        self.key_slider.setValue(len(self._valid_sizes) - 1)
        self.key_slider.setTickPosition(QSlider.TicksBelow)
        self.key_slider.valueChanged.connect(
            lambda i: self.key_val_lbl.setText(f"{self._valid_sizes[i]} бит")
        )
        self.key_val_lbl = QLabel("128 бит")
        self.key_val_lbl.setObjectName("keyValLbl")
        self.key_val_lbl.setFixedWidth(64)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFormat(" %p%")
        self.progress.setFixedHeight(22)
        self.progress.setObjectName("progressBar")

    def _create_layout(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 16)
        root.setSpacing(14)

        title = QLabel("КРИПТОСИСТЕМА")
        title.setObjectName("titleLbl")
        sub = QLabel("RSA-OAEP  ·  CAST5-CBC  ·  PKCS7")
        sub.setObjectName("subLbl")
        root.addWidget(title)
        root.addWidget(sub)
        root.addWidget(self._hline())

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addWidget(self.btn_keygen)
        btn_row.addWidget(self.btn_encrypt)
        btn_row.addWidget(self.btn_decrypt)
        root.addLayout(btn_row)
        root.addWidget(self._hline())

        cfg_lbl = QLabel("ФАЙЛ НАСТРОЕК")
        cfg_lbl.setObjectName("secLbl")
        root.addWidget(cfg_lbl)
        cfg_row = QHBoxLayout()
        cfg_row.setSpacing(6)
        cfg_row.addWidget(self.cfg_path)
        cfg_row.addWidget(self.load_btn)
        cfg_row.addWidget(self.save_btn)
        root.addLayout(cfg_row)
        root.addWidget(self._hline())

        paths_lbl = QLabel("ПУТИ К ФАЙЛАМ")
        paths_lbl.setObjectName("secLbl")
        root.addWidget(paths_lbl)

        grid = QGridLayout()
        grid.setVerticalSpacing(6)
        grid.setHorizontalSpacing(12)
        grid.setColumnMinimumWidth(0, 160)
        path_rows = [
            ("Исходный файл",        self.input_path),
            ("Зашифрованный файл",   self.enc_out_path),
            ("Расшифрованный файл",  self.dec_out_path),
            ("Ключ CAST5  .enc",     self.enc_key_path),
            ("Открытый ключ  .pem",  self.pub_key_path),
            ("Закрытый ключ  .pem",  self.priv_key_path),
        ]
        for i, (lbl_text, widget) in enumerate(path_rows):
            lbl = QLabel(lbl_text)
            lbl.setObjectName("fieldLbl")
            grid.addWidget(lbl, i, 0)
            grid.addWidget(widget, i, 1)
        root.addLayout(grid)
        root.addWidget(self._hline())

        params_lbl = QLabel("ПАРАМЕТРЫ АЛГОРИТМОВ")
        params_lbl.setObjectName("secLbl")
        root.addWidget(params_lbl)

        slider_row = QHBoxLayout()
        lbl_c = QLabel("Длина ключа CAST5")
        lbl_c.setObjectName("fieldLbl")
        lbl_c.setFixedWidth(160)
        slider_row.addWidget(lbl_c)
        slider_row.addWidget(self.key_slider)
        slider_row.addWidget(self.key_val_lbl)
        root.addLayout(slider_row)

        rsa_row = QHBoxLayout()
        lbl_r = QLabel("RSA")
        lbl_r.setObjectName("fieldLbl")
        lbl_r.setFixedWidth(160)
        rsa_val = QLabel("2048 бит  |  e = 65537  |  OAEP + SHA-256")
        rsa_val.setObjectName("infoLbl")
        rsa_row.addWidget(lbl_r)
        rsa_row.addWidget(rsa_val)
        root.addLayout(rsa_row)
        root.addWidget(self._hline())

        root.addWidget(self.progress)

    def _hline(self):
        f = QFrame()
        f.setFrameShape(QFrame.HLine)
        f.setObjectName("hline")
        return f

    def _connect_signals(self):
        self.load_btn.clicked.connect(self._load_config)
        self.save_btn.clicked.connect(self._save_config)
        self.btn_keygen.clicked.connect(self._run_keygen)
        self.btn_encrypt.clicked.connect(self._run_encrypt)
        self.btn_decrypt.clicked.connect(self._run_decrypt)

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a0a0a;
                color: #f0d0d0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QLabel#titleLbl {
                font-size: 26px;
                font-weight: bold;
                color: #ff4444;
            }
            QLabel#subLbl {
                font-size: 11px;
                color: #7a3030;
                margin-bottom: 2px;
            }
            QLabel#secLbl {
                font-size: 10px;
                font-weight: bold;
                color: #cc3333;
                padding-top: 2px;
            }
            QLabel#fieldLbl { color: #885555; font-size: 12px; }
            QLabel#infoLbl  { color: #5a2828; font-size: 12px; }
            QLabel#keyValLbl {
                color: #ff6644;
                font-weight: bold;
                font-size: 13px;
            }
            QFrame#hline {
                color: #3a1010;
                background-color: #3a1010;
                max-height: 1px;
            }
            QLineEdit {
                background-color: #2a0f0f;
                border: 1px solid #5a1a1a;
                border-radius: 4px;
                padding: 5px 8px;
                color: #f0d0d0;
                selection-background-color: #cc3333;
            }
            QLineEdit:focus {
                border-color: #cc3333;
                background-color: #350f0f;
            }
            QPushButton#browseBtn {
                background-color: #2a0f0f;
                border: 1px solid #5a1a1a;
                border-radius: 4px;
                color: #884444;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#browseBtn:hover {
                background-color: #cc3333;
                border-color: #cc3333;
                color: #ffffff;
            }
            QPushButton#mainBtn {
                background-color: #cc3333;
                border: none;
                border-radius: 4px;
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#mainBtn:hover   { background-color: #e04444; }
            QPushButton#mainBtn:pressed { background-color: #991111; }
            QPushButton#mainBtn:disabled {
                background-color: #3a1010;
                color: #5a2020;
            }
            QPushButton#cfgBtn {
                background-color: #2a0f0f;
                border: 1px solid #5a1a1a;
                border-radius: 4px;
                padding: 4px 14px;
                color: #cc6666;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton#cfgBtn:hover {
                background-color: #cc3333;
                border-color: #cc3333;
                color: #ffffff;
            }
            QPushButton#cfgBtn:pressed {
                background-color: #881111;
                color: #ffffff;
            }
            QProgressBar#progressBar {
                background-color: #2a0f0f;
                border: 1px solid #5a1a1a;
                border-radius: 0px;
                color: #ff6666;
                font-size: 11px;
                text-align: left;
            }
            QProgressBar#progressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #881111, stop:1 #ff3333
                );
            }
            QSlider::groove:horizontal {
                height: 3px;
                background: #3a1010;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #cc3333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ff4444;
                border: 1px solid #ff8888;
                width: 12px;
                height: 12px;
                margin: -5px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal:hover { background: #ff8888; }
            QScrollBar:vertical {
                background: #1a0a0a;
                width: 6px;
            }
            QScrollBar::handle:vertical {
                background: #4a1515;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover { background: #cc3333; }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height: 0; }
        """)

    def _apply_settings(self, s):
        """Apply a settings dict to all path fields and the key slider."""
        self.input_path.setText(s.get("input_file", ""))
        self.enc_out_path.setText(s.get("encrypted_file", ""))
        self.dec_out_path.setText(s.get("decrypted_file", ""))
        self.enc_key_path.setText(s.get("encrypted_key_file", ""))
        self.pub_key_path.setText(s.get("public_key_file", ""))
        self.priv_key_path.setText(s.get("private_key_file", ""))
        bits = int(s.get("cast5_key_size", 128))
        if bits in self._valid_sizes:
            self.key_slider.setValue(self._valid_sizes.index(bits))

    def _current_key_size(self):
        return self._valid_sizes[self.key_slider.value()]

    def _log(self, text, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {level}: {text}")

    def _set_busy(self, busy):
        for b in (self.btn_keygen, self.btn_encrypt, self.btn_decrypt):
            b.setEnabled(not busy)

    def _load_config(self):
        path = self.cfg_path.text()
        if not path:
            self._err("Укажите путь к settings.json"); return
        try:
            s = load_settings(path)
            self.settings = s
            self._apply_settings(s)
            self._log(f"Settings loaded: {path}", "OK")
        except Exception as e:
            self._err(e)

    def _save_config(self):
        path = self.cfg_path.text()
        if not path:
            path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить", "settings.json", "JSON (*.json)")
            if not path: return
            self.cfg_path.setText(path)
        try:
            save_settings(path, {
                "input_file":         self.input_path.text(),
                "encrypted_file":     self.enc_out_path.text(),
                "decrypted_file":     self.dec_out_path.text(),
                "encrypted_key_file": self.enc_key_path.text(),
                "public_key_file":    self.pub_key_path.text(),
                "private_key_file":   self.priv_key_path.text(),
                "cast5_key_size":     self._current_key_size(),
            })
            self._log(f"Settings saved: {path}", "OK")
        except Exception as e:
            self._err(e)

    def _start(self, task_fn, ok_msg):
        self._set_busy(True)
        self.progress.setValue(0)
        self._worker = WorkerThread(task_fn)
        self._worker.log_signal.connect(lambda t: self._log(t))
        self._worker.progress_signal.connect(self.progress.setValue)
        self._worker.done_signal.connect(
            lambda ok, e: self._done(ok, e, ok_msg))
        self._worker.start()

    def _done(self, ok, error, ok_msg):
        self._set_busy(False)
        if ok:
            self.progress.setValue(100)
            self._log(ok_msg, "OK")
            QMessageBox.information(self, "Готово", ok_msg)
        else:
            self.progress.setValue(0)
            self._err(error)

    def _check(self, **fields):
        for name, val in fields.items():
            if not val:
                raise ValueError(f"Не указан путь: {name}")

    def _run_keygen(self):
        pub  = self.pub_key_path.text()
        priv = self.priv_key_path.text()
        enc  = self.enc_key_path.text()
        bits = self._current_key_size()
        try:
            self._check(**{"Открытый ключ": pub,
                           "Закрытый ключ": priv,
                           "Файл ключа":    enc})
        except ValueError as e:
            self._err(e); return

        def task(log, prog):
            log.emit("Генерация RSA-ключей (2048 бит)..."); prog.emit(20)
            generate_rsa_keys(pub, priv)
            log.emit(f"Генерация ключа CAST5 ({bits} бит)..."); prog.emit(50)
            sym = generate_cast5_key(bits)
            log.emit("Шифрование ключа CAST5 открытым RSA..."); prog.emit(75)
            encrypt_symmetric_key(sym, pub, enc); prog.emit(100)

        self._start(task, "Ключи успешно созданы")

    def _run_crypto(self, mode):
        """Shared logic for encrypt and decrypt operations."""
        inp  = self.input_path.text() if mode == "encrypt" else self.enc_out_path.text()
        out  = self.enc_out_path.text() if mode == "encrypt" else self.dec_out_path.text()
        priv = self.priv_key_path.text()
        enc  = self.enc_key_path.text()

        field_name = "Исходный файл" if mode == "encrypt" else "Зашифрованный файл"
        result_label = "Зашифрованный файл" if mode == "encrypt" else "Расшифрованный файл"
        file_fn = encrypt_file if mode == "encrypt" else decrypt_file
        ok_msg = f"Файл зашифрован → {out}" if mode == "encrypt" else f"Файл расшифрован → {out}"

        try:
            self._check(**{field_name: inp, "Закрытый ключ": priv,
                           "Файл ключа": enc, result_label: out})
        except ValueError as e:
            self._err(e); return

        def task(log, prog):
            log.emit("Расшифровка ключа CAST5..."); prog.emit(30)
            sym = decrypt_symmetric_key(priv, enc)
            log.emit(f"Операция CAST5-CBC ({get_file_size_str(inp)})..."); prog.emit(60)
            file_fn(inp, out, sym); prog.emit(100)

        self._start(task, ok_msg)

    def _run_encrypt(self):
        self._run_crypto("encrypt")

    def _run_decrypt(self):
        self._run_crypto("decrypt")

    def _err(self, error):
        self._log(f"Error: {error}", "ERR")
        QMessageBox.critical(self, "Ошибка", str(error))


def run_gui(initial_settings=None):
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = CryptoApp(initial_settings=initial_settings)
    w.show()
    sys.exit(app.exec_())


def run_cli():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    except Exception:
        pass

    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема RSA + CAST5'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--keygen',  action='store_true', help='Генерация ключей')
    group.add_argument('--encrypt', action='store_true', help='Шифрование файла')
    group.add_argument('--decrypt', action='store_true', help='Дешифрование файла')

    parser.add_argument('--public_key',    help='Путь к открытому ключу RSA (.pem)')
    parser.add_argument('--private_key',   help='Путь к закрытому ключу RSA (.pem)')
    parser.add_argument('--encrypted_key', help='Путь к зашифрованному симметричному ключу')
    parser.add_argument('--input_file',    help='Путь к входному файлу')
    parser.add_argument('--output_file',   help='Путь для сохранения результата')
    parser.add_argument(
        '--key_size', type=int, default=128, metavar='BITS',
        help='Длина ключа CAST5 в битах: от 40 до 128 с шагом 8 (по умолчанию: 128)'
    )

    args = parser.parse_args()

    match True:
        case _ if args.keygen:
            keygen_mode(args)
        case _ if args.encrypt:
            encrypt_mode(args)
        case _:
            decrypt_mode(args)


def main():
    cli_flags = {'--keygen', '--encrypt', '--decrypt'}
    if any(arg in cli_flags for arg in sys.argv[1:]):
        run_cli()
    else:
        # Настройки считываются здесь, в main, до запуска GUI
        initial_settings = None
        cfg_path = sys.argv[1] if len(sys.argv) > 1 else None
        if cfg_path:
            try:
                initial_settings = load_settings(cfg_path)
            except Exception as e:
                print(f"[WARN] Не удалось загрузить настройки: {e}")
        run_gui(initial_settings=initial_settings)


if __name__ == '__main__':
    main()
