"""Графический интерфейс на tkinter (работает без PyQt5)."""
import tkinter as tk
from tkinter import messagebox, scrolledtext
from hmac_core import compute_hmac, verify_hmac
from constants import DEFAULT_KEY


class HMACApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HMAC - Проверка подлинности сообщений")
        self.root.geometry("700x650")
        self.root.configure(bg="#f0f0f0")
        self.current_hmac = "" 
        self._setup_ui()

    def _setup_ui(self):
        # Заголовок
        title = tk.Label(self.root, text="HMAC-SHA256", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Секретный ключ
        key_frame = tk.LabelFrame(self.root, text="Секретный ключ", bg="#f0f0f0", font=("Arial", 10, "bold"))
        key_frame.pack(fill="x", padx=10, pady=5)
        self.key_entry = tk.Entry(key_frame, width=70, font=("Courier", 10))
        self.key_entry.insert(0, DEFAULT_KEY)
        self.key_entry.pack(padx=10, pady=5, fill="x")

        # Сообщение
        msg_frame = tk.LabelFrame(self.root, text="Сообщение", bg="#f0f0f0", font=("Arial", 10, "bold"))
        msg_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.message_text = scrolledtext.ScrolledText(msg_frame, height=6, font=("Courier", 10))
        self.message_text.pack(padx=10, pady=5, fill="both", expand=True)

        # Кнопки действий
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.compute_btn = tk.Button(btn_frame, text="1. Вычислить HMAC", command=self.compute_hmac,
                                     bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=18)
        self.compute_btn.pack(side="left", padx=5)

        self.modify_btn = tk.Button(btn_frame, text="2. Изменить сообщение", command=self.modify_message,
                                    bg="#FF9800", fg="white", font=("Arial", 10, "bold"), width=18)
        self.modify_btn.pack(side="left", padx=5)

        # Вывод HMAC
        hmac_frame = tk.LabelFrame(self.root, text="Вычисленный HMAC", bg="#f0f0f0", font=("Arial", 10, "bold"))
        hmac_frame.pack(fill="x", padx=10, pady=5)

        self.hmac_display = tk.Entry(hmac_frame, width=80, font=("Courier", 9), fg="blue")
        self.hmac_display.pack(padx=10, pady=5, fill="x")

        # Проверка подлинности
        verify_frame = tk.LabelFrame(self.root, text="Проверка подлинности", bg="#f0f0f0", font=("Arial", 10, "bold"))
        verify_frame.pack(fill="x", padx=10, pady=5)

        # Кнопка автоматической проверки (самая удобная)
        self.auto_verify_btn = tk.Button(verify_frame, text="3. Проверить подлинность (авто)", 
                                         command=self.auto_verify,
                                         bg="#4FF321", fg="white", font=("Arial", 10, "bold"))
        self.auto_verify_btn.pack(pady=10)

        # Разделитель
        tk.Label(verify_frame, text="─" * 60, bg="#f0f0f0").pack(pady=5)

        # Ручной ввод HMAC (на всякий случай)
        tk.Label(verify_frame, text="Или введите HMAC вручную:", bg="#f0f0f0").pack(anchor="w", padx=10)
        self.hmac_check = tk.Entry(verify_frame, width=80, font=("Courier", 9))
        self.hmac_check.pack(padx=10, pady=5, fill="x")

        self.manual_verify_btn = tk.Button(verify_frame, text="Проверить вручную", 
                                           command=self.manual_verify,
                                           bg="#9E9E9E", fg="white", font=("Arial", 9))
        self.manual_verify_btn.pack(pady=5)

    def get_key(self):
        return self.key_entry.get().strip()

    def get_message(self):
        return self.message_text.get("1.0", tk.END).strip()

    def compute_hmac(self):
        try:
            key = self.get_key()
            msg = self.get_message()
            if not key:
                messagebox.showwarning("Ошибка", "Введите секретный ключ")
                return
            if not msg:
                messagebox.showwarning("Ошибка", "Введите сообщение")
                return
            self.current_hmac = compute_hmac(msg, key)
            self.hmac_display.delete(0, tk.END)
            self.hmac_display.insert(0, self.current_hmac)
            messagebox.showinfo("Успех", "HMAC успешно вычислен!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def modify_message(self):
        current = self.get_message()
        if current:
            modified = current + " [ИЗМЕНЕНО]"
        else:
            modified = "Изменённое сообщение"
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert("1.0", modified)
        messagebox.showinfo("Демо", "Сообщение изменено! Теперь нажмите 'Проверить подлинность'.")

    def auto_verify(self):
        """Автоматически проверяет подлинность, используя последний вычисленный HMAC."""
        try:
            key = self.get_key()
            msg = self.get_message()
            
            if not key:
                messagebox.showwarning("Ошибка", "Введите секретный ключ")
                return
            if not msg:
                messagebox.showwarning("Ошибка", "Введите сообщение")
                return
            if not self.current_hmac:
                messagebox.showwarning("Ошибка", "Сначала вычислите HMAC (кнопка 1)")
                return
            
            if verify_hmac(msg, key, self.current_hmac):
                messagebox.showinfo("Результат", " ПОДЛИННОСТЬ ПОДТВЕРЖДЕНА!\n\nСообщение не изменялось, ключ верен.")
            else:
                messagebox.showwarning("Результат", " ПОДЛИННОСТЬ НЕ ПОДТВЕРЖДЕНА!\n\nСообщение было изменено или ключ неверен.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def manual_verify(self):
        """Проверяет с введённым вручную HMAC."""
        try:
            key = self.get_key()
            msg = self.get_message()
            expected = self.hmac_check.get().strip()
            
            if not key:
                messagebox.showwarning("Ошибка", "Введите секретный ключ")
                return
            if not msg:
                messagebox.showwarning("Ошибка", "Введите сообщение")
                return
            if not expected:
                messagebox.showwarning("Ошибка", "Введите HMAC для проверки")
                return
            
            if verify_hmac(msg, key, expected):
                messagebox.showinfo("Результат", "ПОДЛИННОСТЬ ПОДТВЕРЖДЕНА!")
            else:
                messagebox.showwarning("Результат", "ПОДЛИННОСТЬ НЕ ПОДТВЕРЖДЕНА!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def run(self):
        self.root.mainloop()


def run_gui():
    app = HMACApp()
    app.run()


if __name__ == "__main__":
    run_gui()