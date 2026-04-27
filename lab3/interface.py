import argparse
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from crypto_core import (
    create_asymmetric_pair,      
    store_private_key,           
    store_public_key,                  
)

from merge_crypto_system import (
    prepare_encrypted_package, 
    extract_decrypted_package    
)

_CONFIG_PATHS = None
_CRYPTO_PARAMS = None
_USER_PRIVATE_KEY = None
_USER_PUBLIC_KEY = None


def load_config(config_file: str):
    """Загрузка настроек из json - вызывается при запуске программы"""
    global _CONFIG_PATHS, _CRYPTO_PARAMS
    with open(config_file, "r", encoding='utf-8') as f:
        data = json.load(f)
        _CONFIG_PATHS = data.get("paths", {})
        _CRYPTO_PARAMS = data.get("crypto_params", {})


def get_paths():
    """Возвращает путь к настройкам"""
    return _CONFIG_PATHS


def get_crypto_params():
    """Возвращает параметры"""
    return _CRYPTO_PARAMS


def get_private_key_path():
    """Возвращает путь к закрытому ключу (пользовательский или из конфига)"""
    if _USER_PRIVATE_KEY:
        return _USER_PRIVATE_KEY
    private_key_path = _CONFIG_PATHS.get("private_key")
    if not private_key_path:
        raise ValueError("В конфигурации не указан путь для private_key")
    return private_key_path


def get_public_key_path():
    """Возвращает путь к открытому ключу (пользовательский или из конфига)"""
    if _USER_PUBLIC_KEY:
        return _USER_PUBLIC_KEY
    public_key_path = _CONFIG_PATHS.get("public_key")
    if not public_key_path:
        raise ValueError("В конфигурации не указан путь для public_key")
    return public_key_path


def select_private_key():
    global _USER_PRIVATE_KEY
    filename = filedialog.askopenfilename(title="Выберите закрытый ключ", filetypes=[("PEM files", "*.pem")])
    if filename:
        _USER_PRIVATE_KEY = filename
        messagebox.showinfo("Успех", f"Выбран закрытый ключ:\n{filename}")


def select_public_key():
    global _USER_PUBLIC_KEY
    filename = filedialog.askopenfilename(title="Выберите открытый ключ", filetypes=[("PEM files", "*.pem")])
    if filename:
        _USER_PUBLIC_KEY = filename
        messagebox.showinfo("Успех", f"Выбран открытый ключ:\n{filename}")


def reset_keys():
    global _USER_PRIVATE_KEY, _USER_PUBLIC_KEY
    _USER_PRIVATE_KEY = None
    _USER_PUBLIC_KEY = None
    messagebox.showinfo("Успех", "Используются ключи из конфигурации")


def gen_keys():
    """Генерация ключей RSA"""
    paths = get_paths()
    params = get_crypto_params()
    
    private_key, public_key = create_asymmetric_pair(
        key_size=params["rsa_key_size"],
        exponent=params["rsa_public_exponent"]
    )
    
    private_path = paths.get("private_key")
    public_path = paths.get("public_key")
    
    if not private_path or not public_path:
        messagebox.showerror("Ошибка", "В файле конфигурации не указаны пути для ключей")
        return
    
    store_private_key(private_key, private_path)
    store_public_key(public_key, public_path)
    messagebox.showinfo("Успех", f"Ключи созданы:\nЗакрытый: {private_path}\nОткрытый: {public_path}")


def encrypt_file():
    """Шифрование файла"""
    public_key_path = get_public_key_path()
    params = get_crypto_params()
    
    input_file = filedialog.askopenfilename(title="Файл для шифрования")
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(
        title="Имя зашифрованного файла",
        defaultextension=".enc",
        filetypes=[("Encrypted files", "*.enc")])
    if not output_file:
        return
    if not os.path.exists(public_key_path):
        messagebox.showerror("Ошибка", f"Открытый ключ не найден: {public_key_path}")
        return
    
    try:
        prepare_encrypted_package(
            input_file, output_file, public_key_path,
            key_size=params["idea_key_size"],
            iv_size=params["idea_iv_size"],
            block_size_bits=params["idea_block_size_bits"]
        )
        messagebox.showinfo("Успех", f"Зашифрованный файл: {output_file}")
    except Exception as error:
        messagebox.showerror("Ошибка", f"Ошибка шифрования:\n{str(error)}")


def decrypt_file():
    """Расшифрование файла"""
    private_key_path = get_private_key_path()
    params = get_crypto_params()
    
    input_file = filedialog.askopenfilename(
        title="Файл для расшифровки",
        filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")])
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(
        title="Имя расшифрованного файла",
        defaultextension=".txt",
        filetypes=[("All files", "*.*")])
    if not output_file:
        return
    if not os.path.exists(private_key_path):
        messagebox.showerror("Ошибка", f"Закрытый ключ не найден: {private_key_path}")
        return
    
    try:
        extract_decrypted_package(
            input_file, output_file, private_key_path,
            iv_size=params["idea_iv_size"],
            block_size_bits=params["idea_block_size_bits"]
        )
        messagebox.showinfo("Успех", f"Расшифрованный файл: {output_file}")
    except Exception as error:
        messagebox.showerror("Ошибка", f"Ошибка расшифровки:\n{str(error)}")


def create_gui():
    """Создание графического интерфейса"""
    root = tk.Tk()
    root.title("Гибридная криптосистема")
    root.geometry("350x400")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    
    title_label = tk.Label(root, text="Гибридная криптосистема", font=("Arial", 12, "bold"))
    title_label.pack(pady=10)
    subtitle_label = tk.Label(root, text="SEED + RSA", font=("Arial", 9))
    subtitle_label.pack(pady=(0, 10))
    
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x', padx=20, pady=5)
    
    btn_generate = tk.Button(root, text="Генерация ключей", command=gen_keys, width=25, bg="#d0d0d0")
    btn_generate.pack(pady=4)
    
    btn_encrypt = tk.Button(root, text="Шифровка файла", command=encrypt_file, width=25, bg="#d0d0d0")
    btn_encrypt.pack(pady=4)
    
    btn_decrypt = tk.Button(root, text="Расшифровка файла", command=decrypt_file, width=25, bg="#d0d0d0")
    btn_decrypt.pack(pady=4)
    
    sep1 = ttk.Separator(root, orient='horizontal')
    sep1.pack(fill='x', padx=20, pady=8)
    
    btn_sel_private = tk.Button(root, text="Выбрать закрытый ключ", command=select_private_key, width=25, bg="#d0d0d0")
    btn_sel_private.pack(pady=4)
    
    btn_sel_public = tk.Button(root, text="Выбрать открытый ключ", command=select_public_key, width=25, bg="#d0d0d0")
    btn_sel_public.pack(pady=4)
    
    btn_reset = tk.Button(root, text="Сброс к ключам из конфига", command=reset_keys, width=25, bg="#d0d0d0")
    btn_reset.pack(pady=4)
    
    sep2 = ttk.Separator(root, orient='horizontal')
    sep2.pack(fill='x', padx=20, pady=8)
    
    btn_exit = tk.Button(root, text="Завершить сеанс", command=root.quit, width=25, bg="#ff9999", activebackground="#ff6666")
    btn_exit.pack(pady=5)
    
    status_var = tk.StringVar(value="Готов к работе")
    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief='sunken', anchor='w')
    status_bar.pack(side='bottom', fill='x')
    
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема SEED + RSA")
    parser.add_argument("--config", "-c", type=str, default="settings.json",
                        help="Путь к файлу конфигурации (по умолчанию: settings.json)")
    args = parser.parse_args()
    
    if not os.path.exists(args.config):
        print(f"Ошибка: Файл конфигурации {args.config} не найден")
        return
    
    load_config(args.config)
    create_gui()


if __name__ == "__main__":
    main()