import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

import file_io
import scenarios


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Криптосистема ChaCha20+RSA")
        self.geometry("700x550")
        self.configure(bg="#0d1117")
        self.cfg = {}

        tk.Label(self,
                 text="ГИБРИДНАЯ КРИПТОСИСТЕМА",
                 bg="#0d1117",
                 fg="#58a6ff",
                 font=("Arial", 14, "bold")
                 ).pack(pady=(15, 5))

        tk.Label(self,
                 text="ChaCha20 + RSA",
                 bg="#0d1117",
                 fg="#8b949e",
                 font=("Arial", 10)
                 ).pack(pady=(0, 15))

        cfg_frame = tk.Frame(self, bg="#161b22")
        cfg_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(cfg_frame,
                 text="Настройки:",
                 bg="#161b22",
                 fg="#e6edf3",
                 font=("Arial", 10)
                 ).pack(side="left", padx=(10, 5))

        self.cfg_entry = tk.Entry(cfg_frame,
                                  bg="#0d1117",
                                  fg="#e6edf3",
                                  insertbackground="#58a6ff",
                                  relief="flat",
                                  width=45)
        self.cfg_entry.pack(side="left", padx=5)
        self.cfg_entry.insert(0, "settings.json")

        tk.Button(cfg_frame,
                  text="📂",
                  command=self.browse_file,
                  bg="#21262d",
                  fg="#e6edf3",
                  relief="flat",
                  width=3
                  ).pack(side="left", padx=2)

        tk.Button(cfg_frame,
                  text="Загрузить",
                  command=self.load_settings,
                  bg="#238636",
                  fg="#ffffff",
                  relief="flat",
                  padx=10
                  ).pack(side="left", padx=5)

        self.info = tk.Text(self,
                            height=6,
                            bg="#161b22",
                            fg="#8b949e",
                            font=("Courier", 9),
                            relief="flat",
                            padx=10,
                            pady=5)
        self.info.pack(pady=10, padx=20, fill="x")

        btn_frame = tk.Frame(self, bg="#0d1117")
        btn_frame.pack(pady=15)

        btn_params = dict(bg="#21262d", fg="#58a6ff",
                          font=("Arial", 10, "bold"),
                          relief="flat", width=18, padx=10, pady=5)

        self.btn_gen = tk.Button(btn_frame, text="Генерация ключей",
                                  command=self.gen_keys, **btn_params)
        self.btn_gen.pack(side="left", padx=5)

        self.btn_enc = tk.Button(btn_frame, text="Зашифровать",
                                  command=self.encrypt, **btn_params)
        self.btn_enc.pack(side="left", padx=5)

        self.btn_dec = tk.Button(btn_frame, text="Дешифровать",
                                  command=self.decrypt, **btn_params)
        self.btn_dec.pack(side="left", padx=5)

        self._action_buttons = [self.btn_gen, self.btn_enc, self.btn_dec]

        tk.Label(self,
                 text="ЖУРНАЛ СОБЫТИЙ",
                 bg="#0d1117",
                 fg="#8b949e",
                 font=("Arial", 9)
                 ).pack(anchor="w", padx=20, pady=(10, 0))

        self.log = scrolledtext.ScrolledText(self,
                                              bg="#0d1117",
                                              fg="#3fb950",
                                              font=("Courier", 9),
                                              relief="flat",
                                              insertbackground="#58a6ff",
                                              height=12)
        self.log.pack(pady=5, padx=20, fill="both", expand=True)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            self.cfg_entry.delete(0, tk.END)
            self.cfg_entry.insert(0, path)
            self.load_settings()

    def load_settings(self):
        try:
            self.cfg = file_io.load_settings(self.cfg_entry.get())

            self.info.delete(1.0, tk.END)
            self.info.insert(1.0, "ЗАГРУЖЕННЫЕ ПУТИ:\n\n")
            self.info.insert(tk.END, f"  исходный файл:      {self.cfg.get('initial_file', '-')}\n")
            self.info.insert(tk.END, f"  зашифрованный:      {self.cfg.get('encrypted_file', '-')}\n")
            self.info.insert(tk.END, f"  расшифрованный:     {self.cfg.get('decrypted_file', '-')}\n")
            self.info.insert(tk.END, f"  открытый ключ:      {self.cfg.get('public_key', '-')}\n")
            self.info.insert(tk.END, f"  закрытый ключ:      {self.cfg.get('private_key', '-')}")

            self.log_write(f"Настройки загружены: {self.cfg_entry.get()}")
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            messagebox.showerror("Ошибка", str(e))

    def log_write(self, msg: str) -> None:
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def _set_buttons_state(self, state: str) -> None:
        bg = "#161b22" if state == "disabled" else "#21262d"
        for btn in self._action_buttons:
            btn.config(state=state, bg=bg)

    def run_task(self, func, **kwargs) -> None:
        if not self.cfg:
            messagebox.showwarning("Ошибка", "Сначала загрузите settings.json")
            return

        self.log.delete(1.0, tk.END)
        self._set_buttons_state("disabled")
        threading.Thread(target=self._execute, args=(func, kwargs), daemon=True).start()

    def _execute(self, func, kwargs) -> None:
        old_stdout = sys.stdout
        sys.stdout = self
        try:
            func(**kwargs)
            self.after(0, lambda: messagebox.showinfo("Готово", "Операция выполнена успешно"))
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            self.log_write(f"ОШИБКА: {e}")
            self.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        finally:
            sys.stdout = old_stdout
            self.after(0, lambda: self._set_buttons_state("normal"))

    def write(self, msg: str) -> None:
        if msg.strip():
            self.log_write(msg.strip())

    def flush(self) -> None:
        pass

    def gen_keys(self) -> None:
        self.run_task(scenarios.generate_keys,
                      nonce_path=self.cfg["nonce"],
                      encrypted_sym_key_path=self.cfg["encrypted_symmetric_key"],
                      public_key_path=self.cfg["public_key"],
                      private_key_path=self.cfg["private_key"])

    def encrypt(self) -> None:
        self.run_task(scenarios.encrypt_data,
                      input_file=self.cfg["initial_file"],
                      private_key_path=self.cfg["private_key"],
                      encrypted_sym_key_path=self.cfg["encrypted_symmetric_key"],
                      nonce_path=self.cfg["nonce"],
                      output_file=self.cfg["encrypted_file"])

    def decrypt(self) -> None:
        self.run_task(scenarios.decrypt_data,
                      input_file=self.cfg["encrypted_file"],
                      private_key_path=self.cfg["private_key"],
                      encrypted_sym_key_path=self.cfg["encrypted_symmetric_key"],
                      nonce_path=self.cfg["nonce"],
                      output_file=self.cfg["decrypted_file"])


if __name__ == "__main__":
    App().mainloop()
