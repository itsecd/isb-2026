import tkinter as tk
from tkinter import messagebox, filedialog

from crypto_service import (
    generate_keys_service,
    encrypt_service,
    decrypt_service,
)


def run_gui(config: dict) -> None:
    """
    Запускает графический интерфейс.
    """

    def get_key_from_ui():

        match mode_var.get():
            case "manual":
                key = key_entry.get().encode("utf-8")

                if len(key) != 16:
                    messagebox.showerror(
                        "Ошибка",
                        "Ключ должен быть длиной 16 символов",
                    )
                    return None

                return key

            case "random":
                return None

            case _:
                messagebox.showerror(
                    "Ошибка",
                    "Неверный режим выбора ключа",
                )
                return None

    def choose_file():

        file_path = filedialog.askopenfilename()

        if file_path:
            selected_file.set(file_path)

    def generate_keys():

        try:
            key = get_key_from_ui()

            generate_keys_service(
                config=config,
                manual_key=key,
            )

            messagebox.showinfo(
                "Успех",
                "Ключи успешно сгенерированы",
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                str(e),
            )

    def encrypt_file():

        try:
            encrypt_service(
                config=config,
                input_path=selected_file.get(),
            )

            messagebox.showinfo(
                "Успех",
                "Файл успешно зашифрован",
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                str(e),
            )

    def decrypt_file():

        try:
            decrypt_service(config)

            messagebox.showinfo(
                "Успех",
                "Файл успешно расшифрован",
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                str(e),
            )

    root = tk.Tk()

    root.title("Гибридная криптосистема")
    root.geometry("500x550")

    mode_var = tk.StringVar(value="random")

    selected_file = tk.StringVar(value=config["initial_file"])

    encrypted_file = tk.StringVar(value=config["encrypted_file"])

    decrypted_file = tk.StringVar(value=config["decrypted_file"])

    public_key = tk.StringVar(value=config["public_key"])

    private_key = tk.StringVar(value=config["private_key"])

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

    tk.Label(
        root,
        text="Файл для шифрования:",
    ).pack(pady=5)

    tk.Label(
        root,
        textvariable=selected_file,
        wraplength=400,
    ).pack()

    tk.Button(
        root,
        text="Выбрать файл",
        command=choose_file,
    ).pack(pady=5)

    tk.Label(
        root,
        text="Зашифрованный файл:",
    ).pack()

    tk.Label(
        root,
        textvariable=encrypted_file,
        wraplength=400,
    ).pack()

    tk.Label(
        root,
        text="Расшифрованный файл:",
    ).pack()

    tk.Label(
        root,
        textvariable=decrypted_file,
        wraplength=400,
    ).pack()

    tk.Label(
        root,
        text="Публичный ключ:",
    ).pack()

    tk.Label(
        root,
        textvariable=public_key,
        wraplength=400,
    ).pack()

    tk.Label(
        root,
        text="Приватный ключ:",
    ).pack()

    tk.Label(
        root,
        textvariable=private_key,
        wraplength=400,
    ).pack()

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
