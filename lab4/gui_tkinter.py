"""Графический интерфейс на tkinter для работы с HMAC."""
import tkinter as tk
from tkinter import messagebox, scrolledtext
from hmac_core import compute_hmac, verify_hmac
from config_loader import DEFAULT_KEY


class HMACApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HMAC - Проверка подлинности сообщений")
        self.root.geometry("650x550")
        self.root.configure(bg="#f0f0f0")
        self.current_hmac = ""
        self._setup_ui()

    def _setup_ui(self):
        title = tk.Label(self.root, text="HMAC-SHA256", font=("Arial", 14, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        key_frame = tk.LabelFrame(self.root, text="Секретный ключ", bg="#f0f0f0")
        key_frame.pack(fill="x", padx=10, pady=5)
        self.key_entry = tk.Entry(key_frame, width=60)
        self.key_entry.insert(0, DEFAULT_KEY)
        self.key_entry.pack(padx=10, pady=5, fill="x")

        msg_frame = tk.LabelFrame(self.root, text="Сообщение", bg="#f0f0f0")
        msg_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.message_text = scrolledtext.ScrolledText(msg_frame, height=6)
        self.message_text.pack(padx=10, pady=5, fill="both", expand=True)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.compute_btn = tk.Button(btn_frame, text="1. Вычислить HMAC", command=self.compute_hmac,
                                     bg="#4CAF50", fg="white", width=18)
        self.compute_btn.pack(side="left", padx=5)

        self.modify_btn = tk.Button(btn_frame, text="2. Изменить сообщение", command=self.modify_message,
                                    bg="#FF9800", fg="white", width=18)
        self.modify_btn.pack(side="left", padx=5)

        hmac_frame = tk.LabelFrame(self.root, text="Вычисленный HMAC", bg="#f0f0f0")
        hmac_frame.pack(fill="x", padx=10, pady=5)
        self.hmac_display = tk.Entry(hmac_frame, width=70, fg="blue")
        self.hmac_display.pack(padx=10, pady=5, fill="x")

        verify_frame = tk.LabelFrame(self.root, text="Проверка подлинности", bg="#f0f0f0")
        verify_frame.pack(fill="x", padx=10, pady=5)

        self.auto_verify_btn = tk.Button(verify_frame, text="3. Проверить подлинность", command=self.auto_verify,
                                         bg="#2196F3", fg="white")
        self.auto_verify_btn.pack(pady=10)

    def get_key(self):
        return self.key_entry.get().strip()

    def get_message(self):
        return self.message_text.get("1.0", tk.END).strip()

    def compute_hmac(self):
        try:
            key = self.get_key()
            msg = self.get_message()
            if not key or not msg:
                messagebox.showwarning("Ошибка", "Заполните ключ и сообщение")
                return
            self.current_hmac = compute_hmac(msg, key)
            self.hmac_display.delete(0, tk.END)
            self.hmac_display.insert(0, self.current_hmac)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def modify_message(self):
        current = self.get_message()
        modified = current + " [ИЗМЕНЕНО]" if current else "Изменённое сообщение"
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert("1.0", modified)

    def auto_verify(self):
        try:
            key = self.get_key()
            msg = self.get_message()
            if not key or not msg:
                messagebox.showwarning("Ошибка", "Заполните ключ и сообщение")
                return
            if not self.current_hmac:
                messagebox.showwarning("Ошибка", "Сначала вычислите HMAC")
                return
            if verify_hmac(msg, key, self.current_hmac):
                messagebox.showinfo("Результат", " Подлинность подтверждена")
            else:
                messagebox.showwarning("Результат", " Подлинность не подтверждена")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def run(self):
        self.root.mainloop()


def run_gui():
    app = HMACApp()
    app.run()


if __name__ == "__main__":
    run_gui()