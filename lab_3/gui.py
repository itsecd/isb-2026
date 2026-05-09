import os
import customtkinter as ctk
from tkinter import filedialog

from src/file_io import read_file, write_file, load_json
from src/asym_crypto import generate_rsa_keys, encrypt_rsa, decrypt_rsa
from src/sym_crypto import encrypt_seed, decrypt_seed

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hybrid Cryptosystem (RSA + SEED)")
        self.geometry("750x550")
        self.minsize(700, 500)

        try:
            self.settings = load_json('settings.json')
            self.files = self.settings.get('files', {})
            self.params = self.settings.get('crypto_params', {})
        except Exception as e:
            self.files = {}
            self.params = {'rsa_key_size': 2048, 'rsa_public_exponent': 65537, 'seed_key_size': 16,
                           'seed_block_size': 128}
            print(f"Erorro while loading settings.json: {e}")

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Lab№3",
                                        font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=(15, 10))

        self.tabview = ctk.CTkTabview(self, width=700, height=250)
        self.tabview.pack(padx=20, pady=10, fill="x")

        self.tabview.add("Key generation")
        self.tabview.add("Encryption")
        self.tabview.add("Decryption")

        self.setup_generation_tab()
        self.setup_encryption_tab()
        self.setup_decryption_tab()

        self.log_textbox = ctk.CTkTextbox(self, width=700, height=150, state="disabled",
                                          font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.pack(padx=20, pady=(10, 20), fill="both", expand=True)

        self.log("The application is running. The settings are loaded.", "success")

    def setup_generation_tab(self):
        tab = self.tabview.tab("Key generation")

        info = ctk.CTkLabel(tab, text="The keys will be generated and saved by paths from settings.json:\n"
                                      f"Pub: {self.files.get('public_key')}\n"
                                      f"Priv: {self.files.get('secret_key')}\n"
                                      f"Sym: {self.files.get('symmetric_key')}", justify="left")
        info.pack(pady=20)

        btn = ctk.CTkButton(tab, text="Generate keys", command=self.generate_action, width=200, height=40)
        btn.pack(pady=10)

    def setup_encryption_tab(self):
        tab = self.tabview.tab("Encryption")

        self.enc_input_var = ctk.StringVar(value=self.files.get('initial_file', ''))
        self.enc_output_var = ctk.StringVar(value=self.files.get('encrypted_file', ''))

        self.create_file_row(tab, "The source file:", self.enc_input_var)
        self.create_file_row(tab, "Where to save the cipher:", self.enc_output_var, is_save=True)

        btn = ctk.CTkButton(tab, text="Encrypt the data", command=self.encrypt_action, width=200, height=40)
        btn.pack(pady=20)

    def setup_decryption_tab(self):
        tab = self.tabview.tab("Decryption")

        self.dec_input_var = ctk.StringVar(value=self.files.get('encrypted_file', ''))
        self.dec_output_var = ctk.StringVar(value=self.files.get('decrypted_file', ''))

        self.create_file_row(tab, "Encrypted file:", self.dec_input_var)
        self.create_file_row(tab, "Texts save path:", self.dec_output_var, is_save=True)

        btn = ctk.CTkButton(tab, text="Decrypt the data", command=self.decrypt_action, width=200, height=40)
        btn.pack(pady=20)

    def create_file_row(self, parent, label_text, string_var, is_save=False):
        """Auxiliary method for creating a string with a file selection"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)

        lbl = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        lbl.pack(side="left")

        entry = ctk.CTkEntry(frame, textvariable=string_var, width=350, state="disabled")
        entry.pack(side="left", padx=10, fill="x", expand=True)

        def browse():
            if is_save:
                path = filedialog.asksaveasfilename()
            else:
                path = filedialog.askopenfilename()
            if path:
                string_var.set(path)

        btn = ctk.CTkButton(frame, text="View...", width=80, command=browse)
        btn.pack(side="right")

    def log(self, message: str, level: str = "info"):
        """Displaying messages in the logs text window."""
        self.log_textbox.configure(state="normal")

        prefix = "[INFO] "
        if level == "error":
            prefix = "[ERROR] "
        elif level == "success":
            prefix = "[SUCCESS] "

        self.log_textbox.insert("end", prefix + message + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")


    def generate_action(self):
        self.log("Starting of key generation...")
        try:
            pub_key_path = self.files.get('public_key')
            priv_key_path = self.files.get('secret_key')
            sym_key_path = self.files.get('symmetric_key')

            sym_key = os.urandom(self.params.get('seed_key_size', 16))
            pub_bytes, priv_bytes = generate_rsa_keys(
                public_exponent=self.params.get('rsa_public_exponent', 65537),
                key_size=self.params.get('rsa_key_size', 2048)
            )

            write_file(pub_key_path, pub_bytes)
            write_file(priv_key_path, priv_bytes)

            encrypted_sym_key = encrypt_rsa(pub_bytes, sym_key)
            write_file(sym_key_path, encrypted_sym_key)

            self.log(f"RSA keys are saved to: {pub_key_path}, {priv_key_path}", "success")
            self.log(f"The symmetric key (SEED) is encrypted and stored in: {sym_key_path}", "success")
        except Exception as e:
            self.log(str(e), "error")

    def encrypt_action(self):
        self.log("Beginning of data encryption....")
        try:
            input_file = self.enc_input_var.get()
            output_file = self.enc_output_var.get()
            priv_key_path = self.files.get('secret_key')
            sym_key_path = self.files.get('symmetric_key')

            priv_key_pem = read_file(priv_key_path)
            enc_sym_key = read_file(sym_key_path)

            sym_key = decrypt_rsa(priv_key_pem, enc_sym_key)
            self.log("Symmetric key has been successfully decrypted via RSA.")

            plain_text = read_file(input_file)
            iv, cipher_text = encrypt_seed(plain_text, sym_key, self.params.get('seed_block_size', 128))

            write_file(output_file, iv + cipher_text)
            self.log(f"File {input_file} successfully encrypted!", "success")
            self.log(f"The result is saved in: {output_file}", "success")
        except Exception as e:
            self.log(str(e), "error")

    def decrypt_action(self):
        self.log("Beginning of data decryption...")
        try:
            input_file = self.dec_input_var.get()
            output_file = self.dec_output_var.get()
            priv_key_path = self.files.get('secret_key')
            sym_key_path = self.files.get('symmetric_key')

            priv_key_pem = read_file(priv_key_path)
            enc_sym_key = read_file(sym_key_path)

            sym_key = decrypt_rsa(priv_key_pem, enc_sym_key)
            self.log("Symmetric key has been successfully decrypted via RSA.")

            file_content = read_file(input_file)
            if len(file_content) < 16:
                raise ValueError("The file is corrupted: the initialization vector (IV) is missing.")

            iv = file_content[:16]
            cipher_text = file_content[16:]

            plain_text = decrypt_seed(cipher_text, sym_key, iv, self.params.get('seed_block_size', 128))

            write_file(output_file, plain_text)
            self.log(f"File {input_file} successfully decrypted!", "success")
            self.log(f"The result is saved in: {output_file}", "success")
        except Exception as e:
            self.log(str(e), "error")


if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()