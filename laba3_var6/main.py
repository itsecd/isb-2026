#!/usr/bin/env python3
"""
Лабораторная работа №3.
Гибридная криптосистема: SEED (128 бит) + RSA (2048 бит).
"""

import argparse
import sys
from config import ConfigLoader
from file_utils import FileWorker
from seed_cipher import SEEDWrapper
from rsa_manager import RSAProcessor
from exceptions import HybridSystemError


class CryptoHybrid:
    def __init__(self, cfg_path: str = None):
        print("=" * 50)
        print("ЗАПУСК ГИБРИДНОЙ КРИПТОСИСТЕМЫ (SEED+RSA)")
        print("=" * 50)
        try:
            self.cfg = ConfigLoader(cfg_path)
            self.cfg.prepare_folders()
            print("[+] Конфигурация успешно загружена")
        except Exception as err:
            raise HybridSystemError(f"Ошибка старта: {err}")

    def _get_symmetric_key(self) -> bytes:
        print("\n[→] Извлечение симметричного ключа...")
        priv_bytes = FileWorker.read_binary(self.cfg.private_path)
        enc_key_bytes = FileWorker.read_binary(self.cfg.sym_enc_path)
        rsa_obj = RSAProcessor.restore_from_private(priv_bytes)
        sym_key = rsa_obj.decrypt_key(enc_key_bytes)
        return sym_key

    def mode_generate(self):
        print("\n>>> РЕЖИМ 1: ГЕНЕРАЦИЯ КЛЮЧЕЙ <<<\n")
        sym_key = SEEDWrapper.create_key(self.cfg.seed_key_len)
        print(f"  * SEED ключ сгенерирован ({len(sym_key)} байт)")

        rsa_obj = RSAProcessor(
            key_bits=self.cfg.rsa_bits,
            exponent=self.cfg.rsa_exp
        )

        FileWorker.write_binary(self.cfg.public_path, rsa_obj.get_public_pem())
        FileWorker.write_binary(self.cfg.private_path, rsa_obj.get_private_pem())

        encrypted_sym = rsa_obj.encrypt_key(sym_key)
        FileWorker.write_binary(self.cfg.sym_enc_path, encrypted_sym)

        print("\n[✓] КЛЮЧИ СОЗДАНЫ И СОХРАНЕНЫ:")
        print(f"    • Публичный RSA:  {self.cfg.public_path}")
        print(f"    • Приватный RSA:   {self.cfg.private_path}")
        print(f"    • Зашифр. SEED:    {self.cfg.sym_enc_path}")

    def mode_encrypt(self):
        print("\n>>> РЕЖИМ 2: ШИФРОВАНИЕ ФАЙЛА <<<\n")
        sym_key = self._get_symmetric_key()

        cipher = SEEDWrapper(
            key=sym_key,
            block_bits=self.cfg.seed_block_bits,
            iv_len=self.cfg.seed_iv_len
        )
        iv_data = cipher.setup_iv()

        original_text = FileWorker.read_text(self.cfg.input_path)
        original_bytes = original_text.encode(self.cfg.encoding)
        print(f"  * Размер открытого текста: {len(original_bytes)} байт")

        encrypted_result = cipher.process_encrypt(original_bytes)
        print(f"  * Размер шифротекста: {len(encrypted_result)} байт")

        FileWorker.write_binary(self.cfg.encrypted_path, iv_data + encrypted_result)
        print(f"\n[✓] ФАЙЛ ЗАШИФРОВАН: {self.cfg.encrypted_path}")

    def mode_decrypt(self):
        print("\n>>> РЕЖИМ 3: РАСШИФРОВАНИЕ ФАЙЛА <<<\n")
        sym_key = self._get_symmetric_key()

        cipher = SEEDWrapper(
            key=sym_key,
            block_bits=self.cfg.seed_block_bits,
            iv_len=self.cfg.seed_iv_len
        )

        full_data = FileWorker.read_binary(self.cfg.encrypted_path)
        iv_extracted = full_data[:self.cfg.seed_iv_len]
        encrypted_part = full_data[self.cfg.seed_iv_len:]
        print(f"  * IV: {len(iv_extracted)} байт, Данные: {len(encrypted_part)} байт")

        decrypted_bytes = cipher.process_decrypt(encrypted_part, iv_extracted)
        decrypted_text = decrypted_bytes.decode(self.cfg.encoding)
        FileWorker.write_text(self.cfg.decrypted_path, decrypted_text)
        print(f"\n[✓] ФАЙЛ РАСШИФРОВАН: {self.cfg.decrypted_path}")


def make_parser():
    parser = argparse.ArgumentParser(description='Гибридная криптосистема (SEED+RSA)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--generate', action='store_true', help='Сгенерировать ключи')
    group.add_argument('-e', '--encrypt', action='store_true', help='Зашифровать файл')
    group.add_argument('-d', '--decrypt', action='store_true', help='Расшифровать файл')
    parser.add_argument('-c', '--config', default=None, help='Файл конфигурации')
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    try:
        app = CryptoHybrid(args.config)
        if args.generate:
            app.mode_generate()
        elif args.encrypt:
            app.mode_encrypt()
        elif args.decrypt:
            app.mode_decrypt()
    except HybridSystemError as err:
        print(f"\n[ОШИБКА] {err}")
        sys.exit(1)
    except Exception as err:
        print(f"\n[НЕПРЕДВИДЕННАЯ ОШИБКА] {err}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("РАБОТА ЗАВЕРШЕНА УСПЕШНО")
    print("=" * 50)


if __name__ == "__main__":
    main()