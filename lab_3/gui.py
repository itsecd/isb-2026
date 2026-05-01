"""
КИБЕРПАНК-ИНТЕРФЕЙС для гибридной криптосистемы (RSA + SEED).
Запуск:  python gui.py
"""

import json
import os
import random
import threading
import time
import tkinter as tk
from tkinter import filedialog, font as tkfont

from decryption import decrypt
from encryption import encrypt
from generate import generate_key

# ─── палитра ──────────────────────────────────────────────────────────────
BG          = "#07060d"
BG_PANEL    = "#0d0b1a"
NEON_PINK   = "#ff2e88"
NEON_CYAN   = "#00f0ff"
NEON_PURPLE = "#a855f7"
NEON_GREEN  = "#39ff14"
NEON_YELLOW = "#fffb00"
DIM         = "#3a2f5e"
TEXT        = "#e6e1ff"

GLYPHS = "アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF#$%@*"

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "initial_file":   "files/text.txt",
    "encrypted_file": "files/encrypted.txt",
    "decrypted_file": "files/decrypted.txt",
    "symmetric_key":  "files/symmetric.txt",
    "public_key":     "files/public.pem",
    "secret_key":     "files/secret.pem",
}


# ─── matrix-дождь на фоне ─────────────────────────────────────────────────
class MatrixRain:
    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.canvas = canvas
        self.w = width
        self.h = height
        self.font_size = 14
        self.cols = width // self.font_size
        self.drops = [random.randint(-30, 0) for _ in range(self.cols)]
        self.items = []
        self.running = True
        self.tick()

    def tick(self):
        if not self.running:
            return
        for it in self.items:
            self.canvas.delete(it)
        self.items.clear()

        for i in range(self.cols):
            x = i * self.font_size
            head_y = self.drops[i] * self.font_size
            for k in range(12):
                y = head_y - k * self.font_size
                if 0 <= y < self.h:
                    if k == 0:
                        color = NEON_CYAN
                    elif k < 3:
                        color = "#22cc99"
                    elif k < 7:
                        color = "#118866"
                    else:
                        color = "#0a4433"
                    ch = random.choice(GLYPHS)
                    it = self.canvas.create_text(
                        x, y, text=ch, fill=color,
                        font=("Consolas", self.font_size, "bold"),
                        anchor="nw",
                    )
                    self.items.append(it)
            self.drops[i] += 1
            if head_y > self.h + 200 and random.random() > 0.975:
                self.drops[i] = random.randint(-30, 0)

        self.canvas.after(70, self.tick)

    def stop(self):
        self.running = False


# ─── неоновая кнопка ──────────────────────────────────────────────────────
class NeonButton(tk.Canvas):
    def __init__(self, parent, text, color, on_click, width=260, height=70, **kw):
        super().__init__(parent, width=width, height=height, bg=BG_PANEL,
                         highlightthickness=0, **kw)
        self.text = text
        self.color = color
        self.on_click = on_click
        self.w = width
        self.h = height
        self.glow = 0
        self.target_glow = 0
        self.draw()
        self.bind("<Enter>", lambda e: self.set_target(1))
        self.bind("<Leave>", lambda e: self.set_target(0))
        self.bind("<Button-1>", self._click)
        self.animate()

    def set_target(self, v):
        self.target_glow = v

    def _click(self, _e):
        self.flash()
        self.on_click()

    def flash(self):
        self.glow = 1.0
        self.draw()

    def animate(self):
        self.glow += (self.target_glow - self.glow) * 0.15
        self.draw()
        self.after(33, self.animate)

    def draw(self):
        self.delete("all")
        for i in range(6, 0, -1):
            alpha = (0.10 + 0.12 * self.glow) * (i / 6)
            col = blend(BG_PANEL, self.color, alpha)
            self.create_rectangle(
                4 - i, 4 - i, self.w - 4 + i, self.h - 4 + i,
                outline=col, width=1,
            )
        bg = blend(BG_PANEL, self.color, 0.08 + 0.18 * self.glow)
        self.create_rectangle(4, 4, self.w - 4, self.h - 4,
                              fill=bg, outline=self.color, width=2)
        # уголки
        c = self.color
        s = 14
        for (x, y, dx1, dy1, dx2, dy2) in [
            (6, 6, s, 0, 0, s),
            (self.w - 6, 6, -s, 0, 0, s),
            (6, self.h - 6, s, 0, 0, -s),
            (self.w - 6, self.h - 6, -s, 0, 0, -s),
        ]:
            self.create_line(x, y, x + dx1, y + dy1, fill=c, width=3)
            self.create_line(x, y, x + dx2, y + dy2, fill=c, width=3)

        self.create_text(self.w / 2, self.h / 2, text=self.text,
                         fill=TEXT, font=("Consolas", 16, "bold"))


def blend(c1, c2, t):
    """линейная интерполяция двух hex-цветов."""
    t = max(0, min(1, t))
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


# ─── путь-выбиратель ──────────────────────────────────────────────────────
class PathField(tk.Frame):
    def __init__(self, parent, label, color, getter, setter, save_dialog=False):
        super().__init__(parent, bg=BG_PANEL)
        self.color = color
        self.getter = getter
        self.setter = setter
        self.save_dialog = save_dialog

        tk.Label(self, text=label, fg=color, bg=BG_PANEL,
                 font=("Consolas", 10, "bold")).pack(anchor="w")

        row = tk.Frame(self, bg=BG_PANEL)
        row.pack(fill="x", pady=(2, 0))

        self.var = tk.StringVar(value=getter())
        self.var.trace_add("write", lambda *_: setter(self.var.get()))
        self.entry = tk.Entry(
            row, textvariable=self.var, bg="#15102a", fg=TEXT,
            insertbackground=color, relief="flat", font=("Consolas", 10),
            highlightthickness=1, highlightbackground=DIM,
            highlightcolor=color,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=5)

        btn = tk.Label(row, text=" ◇ ", bg="#15102a", fg=color,
                       font=("Consolas", 11, "bold"), cursor="hand2")
        btn.pack(side="right", fill="y")
        btn.bind("<Button-1>", self.browse)
        btn.bind("<Enter>", lambda e: btn.config(fg=NEON_YELLOW))
        btn.bind("<Leave>", lambda e: btn.config(fg=color))

    def browse(self, _):
        if self.save_dialog:
            path = filedialog.asksaveasfilename(initialfile=os.path.basename(self.var.get()))
        else:
            path = filedialog.askopenfilename()
        if path:
            self.var.set(path)


# ─── основное приложение ──────────────────────────────────────────────────
class CryptoUI:
    def __init__(self):
        self.settings = self.load_settings()
        self.root = tk.Tk()
        self.root.title("◢ HYBRID CRYPTO TERMINAL ◣  RSA + SEED")
        self.root.configure(bg=BG)
        self.root.geometry("1180x740")
        self.root.minsize(1100, 700)

        self.build()
        self.boot_sequence()

    # ---- settings -------------------------------------------------------
    def load_settings(self):
        try:
            with open(SETTINGS_FILE) as f:
                s = json.load(f)
            for k, v in DEFAULT_SETTINGS.items():
                s.setdefault(k, v)
            return s
        except FileNotFoundError:
            return dict(DEFAULT_SETTINGS)

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    def get(self, k):
        return self.settings.get(k, DEFAULT_SETTINGS[k])

    def set(self, k, v):
        self.settings[k] = v
        self.save_settings()

    # ---- layout ---------------------------------------------------------
    def build(self):
        # фон с матрицей
        self.bg_canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.update_idletasks()
        self.matrix = MatrixRain(
            self.bg_canvas,
            self.root.winfo_width() or 1180,
            self.root.winfo_height() or 740,
        )
        self.root.bind("<Configure>", self.on_resize)

        # шапка
        header = tk.Frame(self.root, bg=BG)
        header.place(relx=0.5, y=20, anchor="n")
        title_font = ("Consolas", 28, "bold")
        tk.Label(header, text="◢◤  H Y B R I D   C R Y P T O   ◢◤",
                 fg=NEON_PINK, bg=BG, font=title_font).pack()
        tk.Label(header,
                 text="// RSA-2048   ⊕   SEED-CBC   ⊕   ANSI-X9.23 padding",
                 fg=NEON_CYAN, bg=BG, font=("Consolas", 11)).pack(pady=(2, 0))

        # левая панель — пути
        left = tk.Frame(self.root, bg=BG_PANEL,
                        highlightbackground=NEON_PURPLE, highlightthickness=2)
        left.place(x=30, y=110, width=540, height=600)

        tk.Label(left, text="▣  P A T H S",
                 fg=NEON_PURPLE, bg=BG_PANEL,
                 font=("Consolas", 14, "bold")).pack(anchor="w", padx=20, pady=(15, 8))

        for label, key, color, save in [
            ("[ INITIAL FILE ] исходный текст",      "initial_file",   NEON_CYAN,   False),
            ("[ ENCRYPTED ] зашифрованный файл",     "encrypted_file", NEON_PINK,   True),
            ("[ DECRYPTED ] расшифрованный файл",    "decrypted_file", NEON_GREEN,  True),
            ("[ SYM KEY ] симметричный ключ (.bin)", "symmetric_key",  NEON_YELLOW, True),
            ("[ PUBLIC KEY ] открытый ключ (.pem)",  "public_key",     NEON_PURPLE, True),
            ("[ SECRET KEY ] закрытый ключ (.pem)",  "secret_key",     "#ff8855",   True),
        ]:
            f = PathField(
                left, label, color,
                getter=lambda k=key: self.get(k),
                setter=lambda v, k=key: self.set(k, v),
                save_dialog=save,
            )
            f.pack(fill="x", padx=20, pady=6)

        # правая панель — кнопки + лог
        right = tk.Frame(self.root, bg=BG_PANEL,
                         highlightbackground=NEON_CYAN, highlightthickness=2)
        right.place(x=600, y=110, width=550, height=600)

        tk.Label(right, text="▣  C O N T R O L",
                 fg=NEON_CYAN, bg=BG_PANEL,
                 font=("Consolas", 14, "bold")).pack(anchor="w", padx=20, pady=(15, 12))

        btn_row = tk.Frame(right, bg=BG_PANEL)
        btn_row.pack(padx=20, pady=4)

        NeonButton(btn_row, "◈  GENERATE KEYS",  NEON_PURPLE,
                   self.do_generate, width=510, height=58).pack(pady=4)
        NeonButton(btn_row, "▶  ENCRYPT",        NEON_PINK,
                   self.do_encrypt, width=510, height=58).pack(pady=4)
        NeonButton(btn_row, "◀  DECRYPT",        NEON_GREEN,
                   self.do_decrypt, width=510, height=58).pack(pady=4)

        tk.Label(right, text="▣  C O N S O L E",
                 fg=NEON_CYAN, bg=BG_PANEL,
                 font=("Consolas", 14, "bold")).pack(anchor="w", padx=20, pady=(20, 6))

        log_wrap = tk.Frame(right, bg=NEON_CYAN)
        log_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 18))
        self.log = tk.Text(
            log_wrap, bg="#040308", fg=NEON_GREEN,
            font=("Consolas", 10), relief="flat",
            insertbackground=NEON_GREEN, padx=10, pady=8,
        )
        self.log.pack(fill="both", expand=True, padx=2, pady=2)
        self.log.tag_configure("ok",   foreground=NEON_GREEN)
        self.log.tag_configure("err",  foreground=NEON_PINK)
        self.log.tag_configure("info", foreground=NEON_CYAN)
        self.log.tag_configure("warn", foreground=NEON_YELLOW)
        self.log.tag_configure("dim",  foreground=DIM)

        # статус-бар
        self.status_var = tk.StringVar(value="● SYSTEM READY")
        self.status = tk.Label(
            self.root, textvariable=self.status_var,
            fg=NEON_GREEN, bg=BG, font=("Consolas", 10, "bold"),
        )
        self.status.place(x=30, y=720)

        tk.Label(self.root,
                 text="ESC — exit   ◇ — выбор файла",
                 fg=DIM, bg=BG, font=("Consolas", 9),
                 ).place(relx=0.99, y=720, anchor="se")

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.pulse_status()

    def on_resize(self, e):
        if e.widget is self.root:
            self.matrix.w = self.root.winfo_width()
            self.matrix.h = self.root.winfo_height()
            self.matrix.cols = self.matrix.w // self.matrix.font_size
            while len(self.matrix.drops) < self.matrix.cols:
                self.matrix.drops.append(random.randint(-30, 0))

    # ---- лог ------------------------------------------------------------
    def write(self, txt, tag="ok"):
        self.log.insert("end", txt + "\n", tag)
        self.log.see("end")
        self.root.update_idletasks()

    def type_write(self, txt, tag="ok", delay=8):
        for ch in txt:
            self.log.insert("end", ch, tag)
            self.log.see("end")
            self.log.update()
            time.sleep(delay / 1000)
        self.log.insert("end", "\n")

    def boot_sequence(self):
        def run():
            time.sleep(0.2)
            for ln, tag in [
                ("[boot] initializing crypto-core..............", "info"),
                ("[boot] loading RSA-2048 module................", "info"),
                ("[boot] loading SEED-CBC engine................", "info"),
                ("[boot] entropy pool primed....................", "info"),
                ("[ ok ] all systems nominal — awaiting input", "ok"),
                ("", "dim"),
            ]:
                self.write(ln, tag)
                time.sleep(0.07)
        threading.Thread(target=run, daemon=True).start()

    def pulse_status(self):
        t = time.time()
        col = blend(NEON_GREEN, NEON_CYAN, (1 + (t * 2 % 2 - 1)) / 2)
        self.status.configure(fg=col)
        self.root.after(60, self.pulse_status)

    # ---- действия -------------------------------------------------------
    def _ensure_dirs(self, *paths):
        for p in paths:
            d = os.path.dirname(p)
            if d and not os.path.exists(d):
                os.makedirs(d, exist_ok=True)

    def _run_async(self, label, fn, success_msg):
        def task():
            self.status_var.set(f"● {label}...")
            self.write(f">>> {label}", "warn")
            try:
                t0 = time.time()
                fn()
                dt = (time.time() - t0) * 1000
                self.write(f"[ ok ] {success_msg}  ({dt:.0f} ms)", "ok")
                self.write("─" * 56, "dim")
                self.status_var.set("● DONE — SYSTEM READY")
            except Exception as e:
                self.write(f"[err] {type(e).__name__}: {e}", "err")
                self.write("─" * 56, "dim")
                self.status_var.set("● ERROR")
        threading.Thread(target=task, daemon=True).start()

    def do_generate(self):
        sym, pub, sec = self.get("symmetric_key"), self.get("public_key"), self.get("secret_key")
        self._ensure_dirs(sym, pub, sec)
        self._run_async(
            "GENERATING RSA-2048 KEYPAIR + SEED-128 KEY",
            lambda: generate_key(sym, pub, sec),
            f"keys → {sym} | {pub} | {sec}",
        )

    def do_encrypt(self):
        src, sec, sym, dst = (self.get("initial_file"), self.get("secret_key"),
                              self.get("symmetric_key"), self.get("encrypted_file"))
        self._ensure_dirs(dst)
        self._run_async(
            "ENCRYPTING WITH SEED-CBC",
            lambda: encrypt(src, sec, sym, dst),
            f"ciphertext → {dst}",
        )

    def do_decrypt(self):
        enc, sec, sym, dst = (self.get("encrypted_file"), self.get("secret_key"),
                              self.get("symmetric_key"), self.get("decrypted_file"))
        self._ensure_dirs(dst)
        self._run_async(
            "DECRYPTING SEED-CBC PAYLOAD",
            lambda: decrypt(enc, sec, sym, dst),
            f"plaintext → {dst}",
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CryptoUI().run()
