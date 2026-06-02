"""
Main entry point for hybrid cryptosystem command-line interface.

Provides three operational modes:
- Key generation: creates RSA keys and encrypts a symmetric key
- Encryption: encrypts files using hybrid cryptosystem
- Decryption: decrypts files using hybrid cryptosystem

Usage examples:
    python main.py -gen
    python main.py -enc
    python main.py -dec
    python main.py -c custom_settings.json -gen
"""

import argparse
import sys
from config import config, ConfigManager
from key_generator import generate_keys
from encryptor import encrypt_file
from decryptor import decrypt_file
from exceptions import (
    ConfigError,
    KeyGenerationError,
    KeyLoadError,
    EncryptionError,
    DecryptionError,
    FileOperationError,
    PaddingError,
)


def parse_args():
    """
    Parse command-line arguments for the hybrid cryptosystem.

    Defines three operation modes (-gen, -enc, -dec) and optional config path.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing:
            - config: Path to configuration JSON file
            - generation, encryption, decryption: Mode flags

    Command-line syntax:
        -c/--config    Path to config file (default: settings.json)
        -gen           Generate keys
        -enc           Encrypt file
        -dec           Decrypt file
    """
    parser = argparse.ArgumentParser(
        description="Hybrid Crypto System (RSA + SEED-128)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-c", "--config",
        default="settings.json",
        help="Path to configuration JSON file (default: settings.json)"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true", help="Run key generation mode")
    group.add_argument("-enc", "--encryption", action="store_true", help="Run encryption mode")
    group.add_argument("-dec", "--decryption", action="store_true", help="Run decryption mode")

    return parser.parse_args()


def main():
    """
    Main entry point for the hybrid cryptosystem CLI.

    Routes execution to appropriate handler based on operation mode.
    Includes comprehensive error handling for all crypto-related exceptions.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    args = parse_args()

    try:
        global config
        config = ConfigManager(args.config)
    except ConfigError as e:
        print(f"[CONFIG ERROR] {e}", file=sys.stderr)
        return 1

    try:
        if args.generation:
            generate_keys()
        elif args.encryption:
            encrypt_file()
        elif args.decryption:
            decrypt_file()
    except (KeyGenerationError, KeyLoadError, EncryptionError,
            DecryptionError, PaddingError, FileOperationError) as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[INFO] Operation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())