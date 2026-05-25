"""
Резервный tkinter GUI.
"""

import tkinter as tk
from tkinter import messagebox

from crypto_engine import build_hmac


class BackupWindow:
    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Backup HMAC GUI")
        self.root.geometry("500x300")

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self.root, text="Сообщение").pack()

        self.message = tk.Text(self.root, height=5)

        self.message.pack()

        tk.Button(self.root, text="Вычислить", command=self.calculate).pack()

        self.result = tk.Entry(self.root, width=80)

        self.result.pack()

    def calculate(self):

        try:
            text = self.message.get("1.0", tk.END)

            signature = build_hmac(text, "backup_key")

            self.result.delete(0, tk.END)

            self.result.insert(0, signature)

        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def run(self):

        self.root.mainloop()
