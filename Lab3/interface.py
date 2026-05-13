import argparse
import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional, Dict, Any
from contextlib import contextmanager

from RSA_utils import (
    generate_keys,
    serialize_private_key,
    serialize_public_key,
    load_private_key,
    encrypt_with_public_key,
    decrypt_with_private_key,
)
from IDEA_utils import (
    generate_key_for_IDEA,
    generate_iv,
    encrypt_data,
    decrypt_data
)
from file_utils import (
    read_json_file,
    read_binary_file,
    write_binary_file,
    FileOperationError
)
from check_error_utils import (
    handle_errors,
    show_info,
    show_error
)


class SecureKeyManager:
    """Безопасное управление ключами."""
    
    @contextmanager
    def temporary_idea_key(self, enc_key_path: str, priv_key_path: str):
        """Контекстный менеджер для временного использования IDEA ключа."""
        idea_key = None
        encrypted_key = None
        try:
            encrypted_key = read_binary_file(enc_key_path)
            private_key = load_private_key(priv_key_path)
            idea_key = decrypt_with_private_key(encrypted_key, private_key)
            yield idea_key
        finally:
            if idea_key is not None:
                del idea_key
            if encrypted_key is not None:
                del encrypted_key
            import gc
            gc.collect()


class CryptoApplication:
    """Класс для управления гибридной криптосистемой."""
    
    def __init__(self, config_file: str = "settings.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self._full_config = self.config
        
        self._user_private_key_path: Optional[str] = None
        self._user_public_key_path: Optional[str] = None
        self._user_encrypted_key_path: Optional[str] = None
        
        self._key_manager = SecureKeyManager()
        
        self.root: Optional[tk.Tk] = None
        self.status_label: Optional[tk.Label] = None
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            return read_json_file(self.config_file)
        except FileOperationError as e:
            show_error("Критическая ошибка", str(e))
            raise SystemExit(1)
    
    def _get_all_paths(self) -> Dict[str, str]:
        return self._full_config.get("paths", {})
    
    def _get_all_params(self) -> Dict[str, Any]:
        return self._full_config.get("crypto_params", {})
    
    def _get_path_list(self) -> list:
        return list(self._get_all_paths().values())
    
    def _get_param_list(self) -> list:
        return list(self._get_all_params().values())
    
    def _update_status(self, message: str) -> None:
        if self.status_label:
            self.status_label.config(text=message)
            self.root.update_idletasks()
    
    def _get_path_by_position(self, position: int) -> str:
        """Возвращает путь по позиции с учётом пользовательских переопределений."""
        path_values = self._get_path_list()
        path_keys = list(self._get_all_paths().keys())
        
        if position >= len(path_values):
            raise IndexError(f"Путь с позицией {position} не существует")
        if position == 0 and self._user_private_key_path:
            return self._user_private_key_path
        
        if position == 1 and self._user_public_key_path:
            return self._user_public_key_path
        
        if position == 2 and self._user_encrypted_key_path:
            return self._user_encrypted_key_path
        
        return path_values[position]
    
    def _get_param_by_position(self, position: int) -> Any:
        """Возвращает параметр по позиции из crypto_params."""
        param_values = self._get_param_list()
        if position >= len(param_values):
            raise IndexError(f"Параметр с позицией {position} не существует")
        return param_values[position]
    
    @handle_errors("Ошибка генерации ключей")
    def gen_keys(self) -> None:
        """Генерация ключей."""
        self._update_status("Генерация ключей")

        priv_key_path = self._get_path_by_position(1)
        pub_key_path = self._get_path_by_position(0)
        enc_key_path = self._get_path_by_position(2)
        
        rsa_key_size = self._get_param_by_position(0)
        rsa_exponent = self._get_param_by_position(1)
        idea_key_size = self._get_param_by_position(2)
        
        idea_key = generate_key_for_IDEA(idea_key_size)
        private_rsa, public_rsa = generate_keys(rsa_key_size, rsa_exponent)
        
        serialize_private_key(private_rsa, priv_key_path)
        serialize_public_key(public_rsa, pub_key_path)
        
        encrypted_idea_key = encrypt_with_public_key(idea_key, public_rsa)
        write_binary_file(enc_key_path, encrypted_idea_key)
        
        del idea_key
        del encrypted_idea_key
        del private_rsa
        del public_rsa
        
        import gc
        gc.collect()
        self._user_private_key_path = None
        self._user_public_key_path = None
        self._user_encrypted_key_path = None
        
        self._update_status("Ключи сгенерированы")
        show_info("Успех", f"Ключи успешно сгенерированы!\n\n"
                          f"Приватный ключ: {priv_key_path}\n"
                          f"Публичный ключ: {pub_key_path}\n"
                          f"Зашифрованный IDEA ключ: {enc_key_path}")
    
    def encrypt_file(self) -> None:
        """Шифрование файла."""
        input_file = filedialog.askopenfilename(title="Выберите файл для шифрования")
        if not input_file:
            return
        
        self._update_status("Шифрование")
        
        priv_key_path = self._get_path_by_position(0)
        enc_key_path = self._get_path_by_position(2)
        
        iv_size = self._get_param_by_position(3)
        block_size_bits = self._get_param_by_position(4)
        
        plaintext = read_binary_file(input_file)
        
        with self._key_manager.temporary_idea_key(enc_key_path, priv_key_path) as idea_key:
            iv = generate_iv(iv_size)
            ciphertext = encrypt_data(idea_key, iv, plaintext, block_size_bits)
            
            output_file = input_file + ".enc"
            write_binary_file(output_file, iv + ciphertext)
            
            del iv
            del ciphertext
        
        del plaintext
        import gc
        gc.collect()
        
        self._update_status("Шифрование завершено")
        show_info("Успех", f"Файл зашифрован:\n{output_file}")
    
    def decrypt_file(self) -> None:
        """Расшифрование файла."""
        input_file = filedialog.askopenfilename(title="Выберите зашифрованный файл")
        if not input_file:
            return
        
        self._update_status("Расшифрование...")
        
        priv_key_path = self._get_path_by_position(0)
        enc_key_path = self._get_path_by_position(2)
        
        iv_size = self._get_param_by_position(3)
        block_size_bits = self._get_param_by_position(4)
        
        data = read_binary_file(input_file)
        iv = data[:iv_size]
        ciphertext = data[iv_size:]
        
        with self._key_manager.temporary_idea_key(enc_key_path, priv_key_path) as idea_key:
            plaintext = decrypt_data(idea_key, iv, ciphertext, block_size_bits)
            
            output_file = input_file.replace(".enc", ".dec")
            if output_file == input_file:
                output_file = input_file + ".dec"
            
            write_binary_file(output_file, plaintext)
            
            del plaintext
        
        del iv
        del ciphertext
        import gc
        gc.collect()
        
        self._update_status("Расшифрование завершено")
        show_info("Успех", f"Файл расшифрован:\n{output_file}")
    
    def select_private_key(self) -> None:
        """Выбор пользовательского приватного ключа."""
        filename = filedialog.askopenfilename(
            title="Выберите приватный ключ RSA",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
        )
        if filename:
            self._user_private_key_path = filename
            self._update_status("Выбран приватный ключ")
            show_info("Успех", f"Выбран приватный ключ:\n{filename}")
    
    def select_public_key(self) -> None:
        """Выбор пользовательского публичного ключа."""
        filename = filedialog.askopenfilename(
            title="Выберите публичный ключ RSA",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
        )
        if filename:
            self._user_public_key_path = filename
            self._update_status("Выбран публичный ключ")
            show_info("Успех", f"Выбран публичный ключ:\n{filename}")
    
    def select_encrypted_key(self) -> None:
        """Выбор зашифрованного IDEA ключа."""
        filename = filedialog.askopenfilename(
            title="Выберите зашифрованный IDEA ключ",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if filename:
            self._user_encrypted_key_path = filename
            self._update_status("Выбран зашифрованный ключ")
            show_info("Успех", f"Выбран зашифрованный ключ:\n{filename}")
    
    def create_gui(self) -> None:
        """Создаёт графический интерфейс."""
        self.root = tk.Tk()
        self.root.title("Гибридная криптосистема IDEA + RSA")
        self.root.geometry("480x550")
        self.root.resizable(False, False)
        
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            main_frame, 
            text="Гибридное шифрование\nIDEA + RSA", 
            font=("Arial", 14, "bold"),
            justify="center"
        )
        title_label.pack(pady=(0, 15))
        
        buttons = [
            ("Сгенерировать ключи", self.gen_keys),
            ("Выбрать приватный ключ", self.select_private_key),
            ("Выбрать публичный ключ", self.select_public_key),
            ("Выбрать зашифрованный ключ IDEA", self.select_encrypted_key),
            ("Зашифровать файл", self.encrypt_file),
            ("Расшифровать файл", self.decrypt_file),
            ("Выход", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                main_frame,
                text=text,
                command=command,
                width=40,
                height=1,
                bg="#f0f0f0",
                relief=tk.RAISED,
                cursor="hand2",
                font=("Arial", 10)
            )
            btn.pack(pady=4)
            security_note = tk.Label(
            main_frame, 
            text="Ключи не хранятся в памяти, удаляются после использования",
            font=("Arial", 8),
            fg="green"
        )
        security_note.pack(pady=(15, 5))
        self.status_label = tk.Label(
            main_frame,
            text="Готов к работе",
            font=("Arial", 8),
            fg="gray",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        self.root.mainloop()


def main() -> None:
    """Главная функция."""
    parser = argparse.ArgumentParser(description="Гибридная криптосистема IDEA + RSA")
    parser.add_argument(
        "config_file", 
        nargs="?", 
        default="settings.json", 
        help="Путь к файлу конфигурации"
    )
    args = parser.parse_args()
    
    if not os.path.exists(args.config_file):
        print(f"Ошибка: Файл конфигурации {args.config_file} не найден")
        return
    
    app = CryptoApplication(args.config_file)
    app.create_gui()


if __name__ == "__main__":
    main()