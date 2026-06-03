"""Модуль графического интерфейса для криптосистемы. Связывает элементы интерфейса с логикой из модуля facade."""

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict

import facade as crypto_logic


class CryptoApp:
    """Класс, описывающий интерфейс и логику взаимодействия с пользователем."""

    def __init__(self, root: tk.Tk, config_path: str = 'settings.json') -> None:
        """Инициализирует графическое окно и загружает настройки путей.

        Args:
            root (tk.Tk): Корневой объект окна tkinter.
            config_path (str): Путь к JSON-файлу с настройками путей.
        """
        self.root = root
        self.root.title("Гибридная криптосистема: Camellia + RSA")
        self.root.geometry("540x430")
        self.root.resizable(False, False)

        self.config_path = config_path
        self.settings = self._load_settings()

        self._create_widgets()

    def _get_default_settings(self) -> Dict[str, str]:
        """Возвращает стандартную структуру словаря настроек."""
        return {
            'initial_file': 'data.txt',
            'encrypted_file': 'encrypted.dat',
            'decrypted_file': 'decrypted.txt',
            'symmetric_key': 'symmetric_enc.key',
            'public_key': 'public.pem',
            'secret_key': 'private.pem'
        }

    def _load_settings(self) -> Dict[str, str]:
        """Внутренний метод для безопасной загрузки настроек путей."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._get_default_settings()

    def _create_widgets(self) -> None:
        """Создает элементы управления в окне приложения."""
        for widget in self.root.winfo_children():
            widget.destroy()
        frame_config = ttk.LabelFrame(self.root, text=" Управление конфигурацией ", padding=10)
        frame_config.pack(fill="x", padx=15, pady=8)

        self.lbl_config_path = ttk.Label(
            frame_config,
            text=f"Текущий файл: {self.config_path}",
            font=("Arial", 9, "bold"),
            wraplength=480
        )
        self.lbl_config_path.pack(anchor="w", pady=2)
        btn_frame1 = ttk.Frame(frame_config)
        btn_frame1.pack(fill="x", pady=2)

        btn_browse = ttk.Button(
            btn_frame1, text="Выбрать существующий JSON",
            command=self.browse_config_file
        )
        btn_browse.pack(side="left", padx=2, expand=True, fill="x")

        btn_create = ttk.Button(
            btn_frame1, text="Создать новый JSON",
            command=self.create_config_file
        )
        btn_create.pack(side="left", padx=2, expand=True, fill="x")

        btn_frame2 = ttk.Frame(frame_config)
        btn_frame2.pack(fill="x", pady=2)

        btn_edit = ttk.Button(
            btn_frame2, text="Редактировать текущие пути в JSON",
            command=self.open_config_editor
        )
        btn_edit.pack(fill="x", padx=2)
        frame_gen = ttk.LabelFrame(self.root, text=" Подготовка системы ", padding=10)
        frame_gen.pack(fill="x", padx=15, pady=8)

        ttk.Label(frame_gen, text="Длина ключа Camellia:").grid(row=0, column=0, sticky="w")

        self.key_size_var = tk.StringVar(value="256")
        key_combo = ttk.Combobox(
            frame_gen, textvariable=self.key_size_var,
            values=["128", "192", "256"], width=6, state="readonly"
        )
        key_combo.grid(row=0, column=1, padx=10, sticky="w")

        btn_gen = ttk.Button(frame_gen, text="Сгенерировать ключи", command=self.handle_generation)
        btn_gen.grid(row=0, column=2, padx=5, sticky="e")
        frame_ops = ttk.LabelFrame(self.root, text=" Работа с данными ", padding=10)
        frame_ops.pack(fill="x", padx=15, pady=8)

        btn_enc = ttk.Button(
            frame_ops, text="Зашифровать файл",
            width=25, command=self.handle_encryption
        )
        btn_enc.pack(pady=5)

        btn_dec = ttk.Button(
            frame_ops, text="Расшифровать файл",
            width=25, command=self.handle_decryption
        )
        btn_dec.pack(pady=5)

    def browse_config_file(self) -> None:
        """Открывает диалоговое окно для выбора существующего JSON-файла."""
        file_path = filedialog.askopenfilename(
            title="Выберите конфигурационный файл JSON",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            self.config_path = file_path
            self.settings = self._load_settings()
            self._create_widgets()
            messagebox.showinfo("Успех", f"Загружена конфигурация из:\n{file_path}")

    def create_config_file(self) -> None:
        """Позволяет пользователю создать и сохранить новый чистый JSON-файл настроек."""
        file_path = filedialog.asksaveasfilename(
            title="Создать новый файл конфигурации",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )
        if file_path:
            self.config_path = file_path
            self.settings = self._get_default_settings()
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)

            self._create_widgets()
            messagebox.showinfo("Успех", f"Файл создан.\nСейчас откроется редактор для изменения путей.")
            self.open_config_editor()

    def open_config_editor(self) -> None:
        """Открывает дочернее модальное окно для прямого редактирования JSON."""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Редактор настроек")
        editor_window.geometry("450x350")
        editor_window.transient(self.root)
        editor_window.grab_set()

        ttk.Label(
            editor_window,
            text=f"Редактирование путей в файле:\n{self.config_path}",
            justify="left", padding=5, wraplength=420
        ).pack(anchor="w")

        text_area = tk.Text(editor_window, wrap="word", width=50, height=12)
        text_area.pack(padx=10, pady=5, fill="both", expand=True)

        current_json_str = json.dumps(self.settings, indent=4, ensure_ascii=False)
        text_area.insert("1.0", current_json_str)

        def save_json_changes():
            raw_text = text_area.get("1.0", "end-1c")
            try:
                parsed_json = json.loads(raw_text)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(parsed_json, f, indent=4, ensure_ascii=False)

                self.settings = parsed_json
                messagebox.showinfo("Успех", "Конфигурация успешно сохранена!", parent=editor_window)
                editor_window.destroy()
            except json.JSONDecodeError as err:
                messagebox.showerror(
                    "Ошибка синтаксиса",
                    f"Неверный формат JSON! Проверьте синтаксис.\n\nДетали: {err}",
                    parent=editor_window
                )

        btn_save = ttk.Button(editor_window, text="Сохранить изменения", command=save_json_changes)
        btn_save.pack(pady=10)

    def handle_generation(self) -> None:
        """Обработчик кнопки генерации ключей."""
        try:
            size = int(self.key_size_var.get())
            msg = crypto_logic.generate_hybrid_keys(self.settings, size)
            messagebox.showinfo("Успех", msg)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать ключи:\n{e}")

    def handle_encryption(self) -> None:
        """Обработчик кнопки шифрования."""
        try:
            msg = crypto_logic.encrypt_file_hybrid(self.settings)
            messagebox.showinfo("Успех", msg)
        except FileNotFoundError as e:
            messagebox.showerror("Ошибка файла", f"Файл не найден. Проверьте пути.\n{e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Критическая ошибка при шифровании:\n{e}")

    def handle_decryption(self) -> None:
        """Обработчик кнопки дешифрования."""
        try:
            msg = crypto_logic.decrypt_file_hybrid(self.settings)
            messagebox.showinfo("Успех", msg)
        except FileNotFoundError as e:
            messagebox.showerror("Ошибка файла", f"Файл не найден. Проверьте пути.\n{e}")
        except ValueError as e:
            messagebox.showerror("Ошибка данных", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Критическая ошибка при дешифровании:\n{e}")