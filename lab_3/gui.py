import json
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

from decrypt_data import decrypt_with_keys
from encrypt_data import encrypt_with_keys
from key_generator import generate_keys

SETTINGS_FILE = 'settings.json'


class PrintRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Crypto System (Blowfish + RSA)")
        self.root.geometry("700x600")

        self.settings = self.load_settings()

        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_main = ttk.Frame(self.notebook)
        self.tab_files = ttk.Frame(self.notebook)
        self.tab_keys = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_main, text=" Управление ")
        self.notebook.add(self.tab_files, text=" Редактор файлов ")
        self.notebook.add(self.tab_keys, text=" Просмотр ключей ")

        self.setup_main_tab()
        self.setup_files_tab()
        self.setup_keys_tab()

        sys.stdout = PrintRedirector(self.log_area)

    def load_settings(self) -> dict:
        if not os.path.exists(SETTINGS_FILE):
            default_settings = {
                'initial_file': 'text.txt',
                'encrypted_file': 'encrypted.bin',
                'decrypted_file': 'decrypted.txt',
                'symmetric_key': 'symmetric_key.bin',
                'public_key': 'public_key.pem',
                'secret_key': 'secret_key.pem',
                'symmetric_key_length': 128
            }
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=4)
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    # --- ВКЛАДКА 1: ОСНОВНОЕ ---
    def setup_main_tab(self):
        # Настройки длины
        settings_frame = ttk.LabelFrame(self.tab_main, text=" Настройки алгоритма ", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(settings_frame, text="Длина ключа Blowfish:").pack(side="left")
        valid_lengths = [str(i) for i in range(32, 449, 8)]
        self.length_var = tk.StringVar(value=str(self.settings.get('symmetric_key_length', 128)))
        self.length_combo = ttk.Combobox(settings_frame, textvariable=self.length_var, values=valid_lengths,
                                         state="readonly", width=10)
        self.length_combo.pack(side="left", padx=10)

        # Кнопки действий
        btn_frame = ttk.Frame(self.tab_main, padding=10)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Генерировать ключи", command=self.run_gen).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Зашифровать", command=self.run_enc).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Расшифровать", command=self.run_dec).pack(fill="x", pady=2)

        # Лог
        log_frame = ttk.LabelFrame(self.tab_main, text=" Журнал работы ")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True)

    # --- ВКЛАДКА 2: ФАЙЛЫ ---
    def setup_files_tab(self):
        top_frame = ttk.Frame(self.tab_files, padding=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Выберите файл:").pack(side="left")
        self.file_to_edit = tk.StringVar(value="initial_file")
        files_cb = ttk.Combobox(top_frame, textvariable=self.file_to_edit, state="readonly",
                                values=["initial_file", "encrypted_file", "decrypted_file"])
        files_cb.pack(side="left", padx=10)

        files_cb.bind("<<ComboboxSelected>>", self.on_file_selected)

        ttk.Button(top_frame, text="Открыть", command=self.open_file).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Сохранить изменения", command=self.save_file).pack(side="left", padx=5)

        self.file_editor = scrolledtext.ScrolledText(self.tab_files, font=("Consolas", 10))
        self.file_editor.pack(fill="both", expand=True, padx=10, pady=5)

    def on_file_selected(self, event):
        """Очищает редактор при смене файла в списке, чтобы избежать ошибок"""
        self.file_editor.delete(1.0, tk.END)
        self.file_editor.insert(tk.END, f"--- Файл {self.file_to_edit.get()} выбран. Нажмите 'Открыть' ---")

    def open_file(self):
        file_key = self.file_to_edit.get()
        path = self.settings.get(file_key)
        self.file_editor.delete(1.0, tk.END)

        if not os.path.exists(path):
            messagebox.showwarning("Внимание", f"Файл {path} еще не создан.")
            return

        try:
            if file_key == "encrypted_file":
                with open(path, 'rb') as f:
                    content = f.read().hex(' ', 2)
                # Добавляем метку, которую нельзя сохранять
                self.file_editor.insert(tk.END, "--- BINARY HEX VIEW (READ ONLY) ---\n" + content)
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    self.file_editor.insert(tk.END, f.read())
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def save_file(self):
        content = self.file_editor.get(1.0, tk.END).strip()

        # ЗАЩИТА: Не даем сохранить, если это HEX-вид или системное сообщение
        if content.startswith("--- BINARY HEX VIEW") or content.startswith("--- Файл"):
            messagebox.showerror("Ошибка", "Нельзя сохранять HEX-вид или системные сообщения в файл!")
            return

        file_key = self.file_to_edit.get()
        path = self.settings.get(file_key)

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Успех", f"Файл {path} успешно обновлен.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # --- ВКЛАДКА 3: КЛЮЧИ ---
    def setup_keys_tab(self):
        top_frame = ttk.Frame(self.tab_keys, padding=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Ключ:").pack(side="left")
        self.key_to_view = tk.StringVar(value="public_key")
        keys_cb = ttk.Combobox(top_frame, textvariable=self.key_to_view, state="readonly",
                               values=["public_key", "secret_key", "symmetric_key"])
        keys_cb.pack(side="left", padx=10)

        # Кнопка для отображения содержимого
        ttk.Button(top_frame, text="Показать", command=self.view_key).pack(side="left", padx=2)

        # НОВАЯ КНОПКА: Выбрать файл через проводник
        ttk.Button(top_frame, text="Загрузить из файла...", command=self.browse_key).pack(side="left", padx=2)

        self.key_viewer = scrolledtext.ScrolledText(self.tab_keys, font=("Consolas", 10), bg="#f0f0f0")
        self.key_viewer.pack(fill="both", expand=True, padx=10, pady=5)

    def browse_key(self):
        """Открывает диалог выбора файла и обновляет путь к ключу в настройках"""
        key_type = self.key_to_view.get()

        # Определяем расширение файла для удобства поиска
        if key_type == "symmetric_key":
            file_types = [("Binary files", "*.bin"), ("All files", "*.*")]
        else:
            file_types = [("PEM files", "*.pem"), ("All files", "*.*")]

        file_path = filedialog.askopenfilename(title=f"Выберите {key_type}", filetypes=file_types)

        if file_path:
            # Обновляем путь в оперативной памяти
            self.settings[key_type] = file_path

            # Сохраняем в settings.json, чтобы выбор "запомнился"
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)

            print(f"[!] Путь для {key_type} изменен на: {file_path}")

            # Сразу показывае

    def view_key(self):
        key_type = self.key_to_view.get()
        path = self.settings.get(key_type)
        self.key_viewer.config(state="normal")
        self.key_viewer.delete(1.0, tk.END)

        if not os.path.exists(path):
            self.key_viewer.insert(tk.END, "Ключ еще не сгенерирован.")
        else:
            with open(path, 'rb') as f:
                content = f.read()
                if key_type == "symmetric_key":
                    # Он зашифрован RSA, покажем в HEX
                    self.key_viewer.insert(tk.END, "ЗАШИФРОВАННЫЙ КЛЮЧ BLOWFISH (HEX):\n" + content.hex(' ', 4))
                else:
                    # RSA ключи в формате PEM (текст)
                    self.key_viewer.insert(tk.END, content.decode('utf-8'))

        self.key_viewer.config(state="disabled")

    # --- ЛОГИКА ---
    def run_gen(self):
        self.settings['symmetric_key_length'] = int(self.length_var.get())
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)
        print("\n--- Генерация ключей ---")
        generate_keys(self.settings)

    def run_enc(self):
        print("\n--- Шифрование ---")
        encrypt_with_keys(self.settings)

    def run_dec(self):
        try:
            print(f"\n--- Старт расшифровки ---")
            decrypt_with_keys(self.settings)
            messagebox.showinfo("Успех", "Файл успешно расшифрован!")
        except ValueError as e:
            # Чаще всего ValueError на этапе паддинга означает неверный ключ
            print(f"[ОШИБКА ДЕШИФРОВАНИЯ]: {e}")
            messagebox.showerror("Ошибка доступа",
                                 "Не удалось расшифровать файл. \n\n"
                                 "Причина: Скорее всего, ключи были пересозданы, "
                                 "и этот ключ не подходит к зашифрованному файлу.")
        except Exception as e:
            print(f"[ОШИБКА]: {e}")
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    # Немного стилизации
    style = ttk.Style()
    style.configure("TButton", padding=5)
    app = CryptoApp(root)
    root.mainloop()
