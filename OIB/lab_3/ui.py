import json
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from decrypt import decrypt
from encrypt import encrypt
from generate_key import generate_key

SETTINGS_FILE = "settings.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SETTINGS = {
    "symmetric_key": "symmetric_key.bin",
    "public_key": "public_key.pem",
    "secret_key": "secret_key.pem",
    "initial_file": "input.txt",
    "encrypted_file": "encrypted.bin",
    "decrypted_file": "decrypted.txt",
}

def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings: dict) -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

class HybridCryptoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Гибридное шифрование RSA + Camellia")
        self.resizable(False, False)
        self.settings = load_settings()
        self._build_ui()
        self._load_paths()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._tab_gen = ttk.Frame(notebook)
        self._tab_enc = ttk.Frame(notebook)
        self._tab_dec = ttk.Frame(notebook)

        notebook.add(self._tab_gen, text="  Генерация ключей  ")
        notebook.add(self._tab_enc, text="  Шифрование  ")
        notebook.add(self._tab_dec, text="  Дешифрование  ")

        self._build_gen_tab()
        self._build_enc_tab()
        self._build_dec_tab()
        self._build_log_area()

    def _build_gen_tab(self):
        f = self._tab_gen
        pad = {"padx": 8, "pady": 4}

        ttk.Label(f, text="Длина симметричного ключа Camellia:").grid(
            row=0, column=0, columnspan=3, sticky="w", **pad
        )

        self._key_bits = tk.IntVar(value=128)
        for col, bits in enumerate((128, 192, 256)):
            ttk.Radiobutton(f, text=f"{bits} бит", variable=self._key_bits, value=bits).grid(
                row=1, column=col, sticky="w", padx=8
            )

        self._gen_sym  = self._path_row(f, "Симм. ключ (выход):",   2)
        self._gen_pub  = self._path_row(f, "Публичный ключ (выход):", 3, save=False)
        self._gen_priv = self._path_row(f, "Закрытый ключ (выход):", 4, save=False)

        ttk.Button(f, text="Сгенерировать ключи", command=self._run_generate).grid(
            row=5, column=0, columnspan=3, pady=10
        )

    def _build_enc_tab(self):
        f = self._tab_enc
        self._enc_input   = self._path_row(f, "Исходный файл:",        0, open_mode=True)
        self._enc_priv    = self._path_row(f, "Закрытый ключ:",        1, open_mode=True)
        self._enc_sym     = self._path_row(f, "Симм. ключ (зашифр.):", 2, open_mode=True)
        self._enc_output  = self._path_row(f, "Зашифрованный файл:",   3)

        ttk.Button(f, text="Зашифровать", command=self._run_encrypt).grid(
            row=4, column=0, columnspan=3, pady=10
        )

    def _build_dec_tab(self):
        f = self._tab_dec
        self._dec_input   = self._path_row(f, "Зашифрованный файл:",    0, open_mode=True)
        self._dec_priv    = self._path_row(f, "Закрытый ключ:",         1, open_mode=True)
        self._dec_sym     = self._path_row(f, "Симм. ключ (зашифр.):",  2, open_mode=True)
        self._dec_output  = self._path_row(f, "Расшифрованный файл:",   3)

        ttk.Button(f, text="Расшифровать", command=self._run_decrypt).grid(
            row=4, column=0, columnspan=3, pady=10
        )

    def _build_log_area(self):
        frame = ttk.LabelFrame(self, text=" Журнал ")
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._log = scrolledtext.ScrolledText(frame, height=10, state="disabled",
                                              font=("Consolas", 9))
        self._log.pack(fill="both", expand=True, padx=4, pady=4)

        ttk.Button(frame, text="Очистить", command=self._clear_log).pack(
            anchor="e", padx=4, pady=(0, 4)
        )

    def _path_row(self, parent, label: str, row: int,
                  open_mode: bool = False, save: bool = True) -> tk.StringVar:
        var = tk.StringVar()
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=3)
        ttk.Entry(parent, textvariable=var, width=38).grid(row=row, column=1, padx=4)
        cmd = (lambda v=var: self._browse_open(v)) if open_mode else (lambda v=var: self._browse_save(v))
        ttk.Button(parent, text="…", width=3, command=cmd).grid(row=row, column=2, padx=(0, 8))
        return var

    def _browse_open(self, var: tk.StringVar):
        path = filedialog.askopenfilename()
        if path:
            var.set(path)

    def _browse_save(self, var: tk.StringVar):
        path = filedialog.asksaveasfilename()
        if path:
            var.set(path)

    def _load_paths(self):
        s = self.settings
        self._gen_sym.set(s.get("symmetric_key", ""))
        self._gen_pub.set(s.get("public_key", ""))
        self._gen_priv.set(s.get("secret_key", ""))

        self._enc_input.set(s.get("initial_file", ""))
        self._enc_priv.set(s.get("secret_key", ""))
        self._enc_sym.set(s.get("symmetric_key", ""))
        self._enc_output.set(s.get("encrypted_file", ""))

        self._dec_input.set(s.get("encrypted_file", ""))
        self._dec_priv.set(s.get("secret_key", ""))
        self._dec_sym.set(s.get("symmetric_key", ""))
        self._dec_output.set(s.get("decrypted_file", ""))

    def _collect_settings(self):
        self.settings.update({
            "symmetric_key":  self._gen_sym.get(),
            "public_key":     self._gen_pub.get(),
            "secret_key":     self._gen_priv.get(),
            "initial_file":   self._enc_input.get(),
            "encrypted_file": self._enc_output.get(),
            "decrypted_file": self._dec_output.get(),
        })
        save_settings(self.settings)

    def _log_write(self, message: str):
        self._log.configure(state="normal")
        self._log.insert("end", message + "\n")
        self._log.see("end")
        self._log.configure(state="disabled")

    def _clear_log(self):
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")

    def _run_in_thread(self, func):
        """Redirect stdout to log widget and run func in background thread."""
        def worker():
            old_stdout = sys.stdout
            sys.stdout = _LogRedirect(self._log_write)
            try:
                func()
                self.after(0, lambda: messagebox.showinfo("Готово", "Операция выполнена успешно."))
            except Exception as e:
                self.after(0, lambda err=str(e): messagebox.showerror("Ошибка", err))
            finally:
                sys.stdout = old_stdout

        threading.Thread(target=worker, daemon=True).start()

    def _run_generate(self):
        self._collect_settings()
        sym  = self._gen_sym.get()
        pub  = self._gen_pub.get()
        priv = self._gen_priv.get()
        if not (sym and pub and priv):
            messagebox.showwarning("Внимание", "Укажите пути для всех трёх файлов ключей.")
            return
        bits = self._key_bits.get()
        self._run_in_thread(lambda: generate_key(sym, pub, priv, key_bits=bits))

    def _run_encrypt(self):
        self._collect_settings()
        inp  = self._enc_input.get()
        priv = self._enc_priv.get()
        sym  = self._enc_sym.get()
        out  = self._enc_output.get()
        if not (inp and priv and sym and out):
            messagebox.showwarning("Внимание", "Заполните все пути для шифрования.")
            return
        self._run_in_thread(lambda: encrypt(inp, priv, sym, out))

    def _run_decrypt(self):
        self._collect_settings()
        inp  = self._dec_input.get()
        priv = self._dec_priv.get()
        sym  = self._dec_sym.get()
        out  = self._dec_output.get()
        if not (inp and priv and sym and out):
            messagebox.showwarning("Внимание", "Заполните все пути для дешифрования.")
            return
        self._run_in_thread(lambda: decrypt(inp, priv, sym, out))

class _LogRedirect:
    """Redirects print() output to the log widget."""
    def __init__(self, write_fn):
        self._write = write_fn

    def write(self, text: str):
        text = text.rstrip("\n")
        if text:
            self._write(text)

    def flush(self):
        pass

if __name__ == "__main__":
    app = HybridCryptoApp()
    app.mainloop()
