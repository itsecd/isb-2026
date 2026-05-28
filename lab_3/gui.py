import os
import customtkinter as ctk
from tkinter import filedialog

from src.file_io import read_file, write_file, load_json
from src.asym_crypto import generate_rsa_keys, encrypt_rsa, decrypt_rsa
from src.sym_crypto import encrypt_seed, decrypt_seed

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CryptoApp(ctk.CTk):
    def __init__(self):
        """Initialisation function of the window
         Raises:
             Exception: if unexpected error occurs.
        """
        super().__init__()

        self.title("Hybrid Cryptosystem (RSA + SEED)")
        self.geometry("750x570")
        self.minsize(700, 550)

        try:
            self.settings = load_json('settings.json')
            self.files = self.settings.get('files', {})
            self.params = self.settings.get('crypto_params', {})
        except Exception as e:
            self.files = {}
            self.params = {'rsa_key_size': 2048, 'rsa_public_exponent': 65537, 'seed_key_size': 16,
                           'seed_block_size': 128}
            print(f"Failed to load settings.json: {e}")

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets in the window"""
        self.title_label = ctk.CTkLabel(self, text="Lab №3",
                                        font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=(15, 10))

        self.tabview = ctk.CTkTabview(self, width=700, height=270)
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

        self.log("Application started. Settings loaded successfully.", "success")

    def setup_generation_tab(self):
        """Sets up the generation tab"""
        tab = self.tabview.tab("Key generation")

        title_lbl = ctk.CTkLabel(tab, text="Specify the paths to save the generated keys:",
                                 font=ctk.CTkFont(size=14, weight="bold"))
        title_lbl.pack(pady=(10, 5))

        self.gen_pub_var = ctk.StringVar(value=self.files.get('public_key', 'src/public_key.pem'))
        self.gen_priv_var = ctk.StringVar(value=self.files.get('secret_key', 'src/private_key.pem'))
        self.gen_sym_var = ctk.StringVar(value=self.files.get('symmetric_key', 'src/symmetric_key.enc'))

        self.create_file_row(tab, "Public RSA Key:", self.gen_pub_var, is_save=True)
        self.create_file_row(tab, "Private RSA Key:", self.gen_priv_var, is_save=True)
        self.create_file_row(tab, "Symmetric Key:", self.gen_sym_var, is_save=True)

        warning_lbl = ctk.CTkLabel(tab, text="* Note: Existing files at these locations will be overwritten.",
                                   text_color="gray", font=ctk.CTkFont(size=11))
        warning_lbl.pack(pady=(5, 5))

        btn = ctk.CTkButton(tab, text="Generate Keys", command=self.generate_action, width=220, height=35,
                            font=ctk.CTkFont(size=14, weight="bold"))
        btn.pack(pady=(5, 5))

    def setup_encryption_tab(self):
        """Sets up the encryption tab"""
        tab = self.tabview.tab("Encryption")

        self.enc_input_var = ctk.StringVar(value=self.files.get('initial_file', ''))
        self.enc_output_var = ctk.StringVar(value=self.files.get('encrypted_file', ''))

        ctk.CTkLabel(tab, text="Select files for encryption:", font=ctk.CTkFont(size=14, weight="bold")).pack(
            pady=(15, 10))

        self.create_file_row(tab, "Source file:", self.enc_input_var)
        self.create_file_row(tab, "Save cipher to:", self.enc_output_var, is_save=True)

        btn = ctk.CTkButton(tab, text="Encrypt Data", command=self.encrypt_action, width=220, height=35,
                            font=ctk.CTkFont(size=14, weight="bold"))
        btn.pack(pady=(20, 10))

    def setup_decryption_tab(self):
        """Sets up the decryption tab"""
        tab = self.tabview.tab("Decryption")

        self.dec_input_var = ctk.StringVar(value=self.files.get('encrypted_file', ''))
        self.dec_output_var = ctk.StringVar(value=self.files.get('decrypted_file', ''))

        ctk.CTkLabel(tab, text="Select files for decryption:", font=ctk.CTkFont(size=14, weight="bold")).pack(
            pady=(15, 10))

        self.create_file_row(tab, "Encrypted file:", self.dec_input_var)
        self.create_file_row(tab, "Save text to:", self.dec_output_var, is_save=True)

        btn = ctk.CTkButton(tab, text="Decrypt Data", command=self.decrypt_action, width=220, height=35,
                            font=ctk.CTkFont(size=14, weight="bold"))
        btn.pack(pady=(20, 10))

    def create_file_row(self, parent, label_text, string_var, is_save=False)->None:
        """
        Creates the file row in the window.
        Args:
            parent (tkinter.Frame): The parent window
            label_text (tkinter.Label): The text label
            string_var (tkinter.StringVar): The string variable
            is_save (bool): If true, save the file
        Returns:
            None
        """
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)

        lbl = ctk.CTkLabel(frame, text=label_text, width=130, anchor="w")
        lbl.pack(side="left")

        entry = ctk.CTkEntry(frame, textvariable=string_var, width=350, state="disabled")
        entry.pack(side="left", padx=10, fill="x", expand=True)

        def browse():
            """Browses the path"""
            if is_save:
                path = filedialog.asksaveasfilename()
            else:
                path = filedialog.askopenfilename()
            if path:
                string_var.set(path)

        btn = ctk.CTkButton(frame, text="Browse...", width=80, command=browse)
        btn.pack(side="right")

    def log(self, message: str, level: str = "info"):
        """Writes a message to the log window
            Args:
                message (str): The message to log
                level (str): The log level

        """
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
        """Generates the key
            Raises:
                Exception: if generation fails"""
        self.log("Starting key generation...")
        try:
            pub_key_path = self.gen_pub_var.get()
            priv_key_path = self.gen_priv_var.get()
            sym_key_path = self.gen_sym_var.get()

            sym_key = os.urandom(self.params.get('seed_key_size', 16))
            pub_bytes, priv_bytes = generate_rsa_keys(
                public_exponent=self.params.get('rsa_public_exponent', 65537),
                key_size=self.params.get('rsa_key_size', 2048)
            )

            write_file(pub_key_path, pub_bytes)
            write_file(priv_key_path, priv_bytes)

            encrypted_sym_key = encrypt_rsa(pub_bytes, sym_key)
            write_file(sym_key_path, encrypted_sym_key)

            self.log(f"RSA keys saved to: {pub_key_path} and {priv_key_path}", "success")
            self.log(f"Symmetric SEED key encrypted and saved to: {sym_key_path}", "success")
        except Exception as e:
            self.log(f"Generation error: {e}", "error")

    def encrypt_action(self):
        """Encrypts the file
            Raises:
                Exception: if encryption fails"""
        self.log("Starting data encryption...")
        try:
            input_file = self.enc_input_var.get()
            output_file = self.enc_output_var.get()
            priv_key_path = self.files.get('secret_key')
            sym_key_path = self.files.get('symmetric_key')

            priv_key_pem = read_file(priv_key_path)
            enc_sym_key = read_file(sym_key_path)

            sym_key = decrypt_rsa(priv_key_pem, enc_sym_key)
            self.log("Symmetric key successfully decrypted via RSA.")

            plain_text = read_file(input_file)
            iv, cipher_text = encrypt_seed(plain_text, sym_key, self.params.get('seed_block_size', 128))

            write_file(output_file, iv + cipher_text)
            self.log(f"File '{os.path.basename(input_file)}' encrypted successfully!", "success")
            self.log(f"Result saved to: {output_file}", "success")
        except Exception as e:
            self.log(f"Encryption error: {e}", "error")

    def decrypt_action(self):
        """Decrypts the file
            Raises:
                Exception: if decryption fails
        """
        self.log("Starting data decryption...")
        try:
            input_file = self.dec_input_var.get()
            output_file = self.dec_output_var.get()
            priv_key_path = self.files.get('secret_key')
            sym_key_path = self.files.get('symmetric_key')

            priv_key_pem = read_file(priv_key_path)
            enc_sym_key = read_file(sym_key_path)

            sym_key = decrypt_rsa(priv_key_pem, enc_sym_key)
            self.log("Symmetric key successfully decrypted via RSA.")

            file_content = read_file(input_file)
            if len(file_content) < 16:
                raise ValueError("File is corrupted: Initialization Vector (IV) is missing.")

            iv = file_content[:16]
            cipher_text = file_content[16:]

            plain_text = decrypt_seed(cipher_text, sym_key, iv, self.params.get('seed_block_size', 128))

            write_file(output_file, plain_text)
            self.log(f"File '{os.path.basename(input_file)}' decrypted successfully!", "success")
            self.log(f"Result saved to: {output_file}", "success")
        except Exception as e:
            self.log(f"Decryption error: {e}", "error")


if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()