import tkinter as tk
from tkinter import messagebox

from crypto_service import (
    generate_keys_service,
    encrypt_file_service,
    decrypt_file_service,
)


def run_gui(config: dict) -> None:
    """
    Запускает графический интерфейс.
    """

    def generate_keys():
        try:
            match mode_var.get():
                case "manual":
                    key = key_entry.get()

                    if len(key) != 16:
                        messagebox.showerror(
                            "Ошибка",
                            "Ключ должен быть 16 символов",
                        )
                        return

                    generate_keys_service(
                        config,
                        key.encode("utf-8"),
                    )

                case "random":
                    generate_keys_service(config)

                case _:
                    messagebox.showerror(
                        "Ошибка",
                        "Неверный режим",
                    )
                    return

            messagebox.showinfo(
                "Успех",
                "Ключи сгенерированы",
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                str(e),
            )

    def encrypt_file():
        try:
            encrypt_file_service(config)

            messagebox.showinfo(
                "Успех",
                "Файл зашифрован",
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                str(e),
            )

    def decrypt_file():
        try:
            decrypt_file_service(config)

            messagebox.showinfo(
                "Успех",
                "Файл расшифрован",
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                str(e),
            )

    root = tk.Tk()

    root.title("Гибридная криптосистема")
    root.geometry("400x300")

    mode_var = tk.StringVar(value="random")

    tk.Label(
        root,
        text="Выбор ключа:",
    ).pack(pady=5)

    tk.Radiobutton(
        root,
        text="Сгенерировать",
        variable=mode_var,
        value="random",
    ).pack()

    tk.Radiobutton(
        root,
        text="Ввести вручную",
        variable=mode_var,
        value="manual",
    ).pack()

    tk.Label(
        root,
        text="Ключ (16 символов):",
    ).pack(pady=5)

    key_entry = tk.Entry(
        root,
        width=30,
    )

    key_entry.pack()

    tk.Button(
        root,
        text="Генерация ключей",
        command=generate_keys,
    ).pack(pady=5)

    tk.Button(
        root,
        text="Шифровать",
        command=encrypt_file,
    ).pack(pady=5)

    tk.Button(
        root,
        text="Дешифровать",
        command=decrypt_file,
    ).pack(pady=5)

    root.mainloop()
