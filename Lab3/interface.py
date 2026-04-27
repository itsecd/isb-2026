import argparse
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from RSA_utils import (
    generate_keys,
    serialize_private_key,
    serialize_public_key,
    load_private_key,
    encrypt_with_public_key,
    decrypt_with_private_key
)
from IDEA_utils import (
    generate_key_for_IDEA,
    generate_IV,
    make_padding,
    make_unpadding,
    encrypt_data,
    decrypt_data
)


_CONFIG_DATA = None


def load_config(config_file: str):
    global _CONFIG_DATA
    with open(config_file, "r", encoding='utf-8') as f:
        _CONFIG_DATA = json.load(f)


def get_paths():
    return _CONFIG_DATA.get("paths", {})


def get_crypto_params():
    return _CONFIG_DATA.get("crypto_params", {})


user_private_key = None
user_public_key = None
user_encrypted_key = None


def gen_keys():
    p = get_paths()
    idea_key = generate_key_for_IDEA()
    priv, pub = generate_keys()
    serialize_private_key(priv, p["private_key"])
    serialize_public_key(pub, p["public_key"])
    encrypted = encrypt_with_public_key(idea_key, pub)
    with open(p["encrypted_key"], "wb") as f:
        f.write(encrypted)
    messagebox.showinfo("Ключи сгенерированы")


def select_private_key():
    global user_private_key
    filename = filedialog.askopenfilename(title="Приватный ключ")
    if filename:
        user_private_key = filename
        messagebox.showinfo("Успех", f"Приватный ключ: {filename}")


def select_public_key():
    global user_public_key
    filename = filedialog.askopenfilename(title="Публичный ключ")
    if filename:
        user_public_key = filename
        messagebox.showinfo("Успех", f"Публичный ключ: {filename}")


def select_encrypted_key():
    global user_encrypted_key
    filename = filedialog.askopenfilename(title="Зашифрованный ключ IDEA")
    if filename:
        user_encrypted_key = filename
        messagebox.showinfo("Успех", f"Зашифрованный ключ: {filename}")


def encrypt_file():
    p = get_paths()
    params = get_crypto_params()
    
    priv_path = user_private_key if user_private_key else p["private_key"]
    enc_key_path = user_encrypted_key if user_encrypted_key else p["encrypted_key"]
    
    if not os.path.exists(priv_path):
        messagebox.showerror("Ошибка", "Приватный ключ не найден")
        return
    if not os.path.exists(enc_key_path):
        messagebox.showerror("Ошибка", "Зашифрованный ключ не найден")
        return
    
    input_file = filedialog.askopenfilename(title="Файл для шифрования")
    if not input_file:
        return
    with open(enc_key_path, "rb") as f:
        encrypted_key = f.read()
    priv = load_private_key(priv_path)
    idea_key = decrypt_with_private_key(encrypted_key, priv)
    with open(input_file, "rb") as f:
        plain = f.read()
        iv_size = params.get("idea_iv_size", 8)
    block_size_bits = params.get("idea_block_size_bits", 64)
    
    iv = generate_IV(iv_size)
    padded = make_padding(plain, block_size_bits)
    cipher = encrypt_data(idea_key, iv, padded, block_size_bits)
    output_file = input_file + ".enc"
    with open(output_file, "wb") as f:
        f.write(iv)
        f.write(cipher)
    messagebox.showinfo("Успех", f"Зашифрованный файл: {output_file}")


def decrypt_file():
    p = get_paths()
    params = get_crypto_params()
    
    priv_path = user_private_key if user_private_key else p["private_key"]
    enc_key_path = user_encrypted_key if user_encrypted_key else p["encrypted_key"]
    
    if not os.path.exists(priv_path):
        messagebox.showerror("Ошибка", "Приватный ключ не найден")
        return
    if not os.path.exists(enc_key_path):
        messagebox.showerror("Ошибка", "Зашифрованный ключ не найден")
        return
    
    input_file = filedialog.askopenfilename(title="Файл для расшифрования")
    if not input_file:
        return
    with open(enc_key_path, "rb") as f:
        encrypted_key = f.read()
    priv = load_private_key(priv_path)
    idea_key = decrypt_with_private_key(encrypted_key, priv)
    with open(input_file, "rb") as f:
        iv_size = params.get("idea_iv_size", 8)
        iv = f.read(iv_size)
        cipher = f.read()
    
    block_size_bits = params.get("idea_block_size_bits", 64)
    decrypted = decrypt_data(idea_key, iv, cipher, block_size_bits)
    plain = make_unpadding(decrypted, block_size_bits)
    output_file = input_file.replace(".enc", ".dec")
    with open(output_file, "wb") as f:
        f.write(plain)
    messagebox.showinfo("Успех", f"Расшифрованный файл: {output_file}")


def create_gui():
    root = tk.Tk()
    root.title("Hybrid Crypto")
    root.geometry("300x280")
    
    tk.Button(root, text="Generate Keys", command=gen_keys, width=25).pack(pady=5)
    tk.Button(root, text="Select Private Key", command=select_private_key, width=25).pack(pady=5)
    tk.Button(root, text="Select Public Key", command=select_public_key, width=25).pack(pady=5)
    tk.Button(root, text="Select Encrypted Key", command=select_encrypted_key, width=25).pack(pady=5)
    tk.Button(root, text="Encrypt File", command=encrypt_file, width=25).pack(pady=5)
    tk.Button(root, text="Decrypt File", command=decrypt_file, width=25).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, width=25).pack(pady=5)
    
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема IDEA + RSA")
    parser.add_argument("config_file", nargs="?", default="settings.json",
                        help="Путь к файлу конфигурации (по умолчанию: settings.json)")
    args = parser.parse_args()
    
    if not os.path.exists(args.config_file):
        print(f"Ошибка: Файл конфигурации {args.config_file} не найден")
        return
    
    load_config(args.config_file)
    create_gui()


if __name__ == "__main__":
    main()