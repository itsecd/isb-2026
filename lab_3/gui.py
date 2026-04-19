import json
import tkinter as tk
from tkinter import messagebox

from crypto_utils import (
    generate_idea_key,
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    encrypt_key,
    decrypt_key,
    encrypt_data,
    decrypt_data,
    load_private_key,
)


with open("settings.json") as f:
    config = json.load(f)


def get_key_from_ui():
    if mode_var.get() == "manual":
        key = key_entry.get().encode("utf-8")

        if len(key) != 16:
            messagebox.showerror("Ошибка", "Ключ должен быть 16 символов")
            return None

        return key
    else:
        return generate_idea_key()


def generate_keys():
    try:
        sym_key = get_key_from_ui()
        if sym_key is None:
            return

        private_key, public_key = generate_rsa_keys()

        save_private_key(private_key, config["private_key"])
        save_public_key(public_key, config["public_key"])

        enc_key = encrypt_key(public_key, sym_key)

        with open(config["symmetric_key"], "wb") as f:
            f.write(enc_key)

        messagebox.showinfo("Успех", "Ключи сгенерированы")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def encrypt_file():
    try:
        private_key = load_private_key(config["private_key"])

        with open(config["symmetric_key"], "rb") as f:
            enc_key = f.read()

        sym_key = decrypt_key(private_key, enc_key)

        with open(config["initial_file"], "rb") as f:
            data = f.read()

        encrypted = encrypt_data(sym_key, data)

        with open(config["encrypted_file"], "wb") as f:
            f.write(encrypted)

        messagebox.showinfo("Успех", "Файл зашифрован")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def decrypt_file():
    try:
        private_key = load_private_key(config["private_key"])

        with open(config["symmetric_key"], "rb") as f:
            enc_key = f.read()

        sym_key = decrypt_key(private_key, enc_key)

        with open(config["encrypted_file"], "rb") as f:
            data = f.read()

        decrypted = decrypt_data(sym_key, data)

        with open(config["decrypted_file"], "wb") as f:
            f.write(decrypted)

        messagebox.showinfo("Успех", "Файл расшифрован")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


root = tk.Tk()
root.title("Гибридная криптосистема")
root.geometry("400x300")


mode_var = tk.StringVar(value="random")

tk.Label(root, text="Выбор ключа:").pack(pady=5)

tk.Radiobutton(root, text="Сгенерировать", variable=mode_var, value="random").pack()
tk.Radiobutton(root, text="Ввести вручную", variable=mode_var, value="manual").pack()


tk.Label(root, text="Ключ (16 символов):").pack(pady=5)
key_entry = tk.Entry(root, width=30)
key_entry.pack()

# кнопки
tk.Button(root, text="Генерация ключей", command=generate_keys).pack(pady=5)
tk.Button(root, text="Шифровать", command=encrypt_file).pack(pady=5)
tk.Button(root, text="Дешифровать", command=decrypt_file).pack(pady=5)

root.mainloop()
