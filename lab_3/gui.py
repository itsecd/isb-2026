import tkinter as tk
from tkinter import messagebox


from crypto.symmetric import (
    generate_idea_key,
    encrypt_data,
    decrypt_data,
)

from crypto.asymmetric import (
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    load_private_key,
    encrypt_key,
    decrypt_key,
)

from file_utils import read_file, write_file


def run_gui(config: dict) -> None:
    """
    Запускает графический интерфейс.
    """

    def get_key_from_ui():
        match mode_var.get():
            case "manual":
                key = key_entry.get().encode("utf-8")

                if len(key) != 16:
                    messagebox.showerror("Ошибка", "Ключ должен быть 16 символов")
                    return None

                return key

            case "random":
                return generate_idea_key()

            case _:
                messagebox.showerror("Ошибка", "Неверный режим")
                return None

    def load_sym_key():
        private_key = load_private_key(config["private_key"])
        enc_key = read_file(config["symmetric_key"])
        return decrypt_key(private_key, enc_key)

    def generate_keys():
        try:
            sym_key = get_key_from_ui()
            if sym_key is None:
                return

            private_key, public_key = generate_rsa_keys()

            save_private_key(private_key, config["private_key"])
            save_public_key(public_key, config["public_key"])

            enc_key = encrypt_key(public_key, sym_key)
            write_file(config["symmetric_key"], enc_key)

            messagebox.showinfo("Успех", "Ключи сгенерированы")

        except Exception as e:
            messagebox.showerror("Ошибка", f"{e}")

    def encrypt_file():
        try:
            sym_key = load_sym_key()

            data = read_file(config["initial_file"])
            encrypted = encrypt_data(sym_key, data)

            write_file(config["encrypted_file"], encrypted)

            messagebox.showinfo("Успех", "Файл зашифрован")

        except Exception as e:
            messagebox.showerror("Ошибка", f"{e}")

    def decrypt_file():
        try:
            sym_key = load_sym_key()

            data = read_file(config["encrypted_file"])
            decrypted = decrypt_data(sym_key, data)

            write_file(config["decrypted_file"], decrypted)

            messagebox.showinfo("Успех", "Файл расшифрован")

        except Exception as e:
            messagebox.showerror("Ошибка", f"{e}")

    # GUI
    root = tk.Tk()
    root.title("Гибридная криптосистема")
    root.geometry("400x300")

    mode_var = tk.StringVar(value="random")

    tk.Label(root, text="Выбор ключа:").pack(pady=5)

    tk.Radiobutton(root, text="Сгенерировать", variable=mode_var, value="random").pack()
    tk.Radiobutton(
        root, text="Ввести вручную", variable=mode_var, value="manual"
    ).pack()

    tk.Label(root, text="Ключ (16 символов):").pack(pady=5)
    key_entry = tk.Entry(root, width=30)
    key_entry.pack()

    tk.Button(root, text="Генерация ключей", command=generate_keys).pack(pady=5)
    tk.Button(root, text="Шифровать", command=encrypt_file).pack(pady=5)
    tk.Button(root, text="Дешифровать", command=decrypt_file).pack(pady=5)

    root.mainloop()
