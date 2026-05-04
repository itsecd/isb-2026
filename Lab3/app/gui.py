import tkinter as tk
from tkinter import filedialog, messagebox

from app.symmetric import generate_cast5_key, encrypt_file, decrypt_file
from app.asymmetric import (
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    load_private_key,
    load_public_key,
    encrypt_symmetric_key,
    decrypt_symmetric_key
)
from app.file_utils import write_bytes, read_bytes


class App:
    def __init__(self, root, config: dict):
        self.root = root
        self.config = config

        self.root.title("Гибридная криптосистема")
        self.root.geometry("400x400")

        self.key_size_var = tk.IntVar(value=config["default_key_size_bits"])
        self.file_path_var = tk.StringVar()

        self.build_ui()

    # UI
    def build_ui(self):
        tk.Label(self.root, text="Выбор файла").pack(pady=5)

        tk.Entry(self.root, textvariable=self.file_path_var, width=40).pack()
        tk.Button(self.root, text="Обзор", command=self.choose_file).pack(pady=5)

        tk.Label(self.root, text="Длина ключа CAST5 (бит)").pack(pady=5)

        tk.OptionMenu(
            self.root,
            self.key_size_var,
            *self.config["allowed_key_sizes_bits"]
        ).pack()

        tk.Button(self.root, text="Сгенерировать ключи", command=self.generate_keys).pack(pady=10)
        tk.Button(self.root, text="Зашифровать", command=self.encrypt_action).pack(pady=5)
        tk.Button(self.root, text="Расшифровать", command=self.decrypt_action).pack(pady=5)

    def choose_file(self):
        path = filedialog.askopenfilename()
        self.file_path_var.set(path)

    def generate_keys(self):
        try:
            key_size = self.key_size_var.get()

            sym_key = generate_cast5_key(key_size)
            write_bytes(self.config["symmetric_key"], sym_key)

            private_key, public_key = generate_rsa_keys(self.config["rsa_key_size_bits"])

            save_private_key(private_key, self.config["private_key"])
            save_public_key(public_key, self.config["public_key"])

            enc_key = encrypt_symmetric_key(public_key, sym_key)
            write_bytes(self.config["encrypted_symmetric_key"], enc_key)

            messagebox.showinfo("OK", "Ключи успешно сгенерированы")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def encrypt_action(self):
        try:
            input_path = self.file_path_var.get()

            if not input_path:
                raise ValueError("Выберите файл")

            private_key = load_private_key(self.config["private_key"])
            enc_key = read_bytes(self.config["encrypted_symmetric_key"])

            sym_key = decrypt_symmetric_key(private_key, enc_key)

            encrypt_file(
                input_path,
                self.config["encrypted_file"],
                sym_key
            )

            messagebox.showinfo("OK", "Файл зашифрован")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def decrypt_action(self):
        try:
            private_key = load_private_key(self.config["private_key"])
            enc_key = read_bytes(self.config["encrypted_symmetric_key"])

            sym_key = decrypt_symmetric_key(private_key, enc_key)

            decrypt_file(
                self.config["encrypted_file"],
                self.config["decrypted_file"],
                sym_key
            )

            messagebox.showinfo("OK", "Файл расшифрован")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))