import argparse
import os

from src/file_io import read_file, write_file, load_json
from src/asym_crypto import generate_rsa_keys, encrypt_rsa, decrypt_rsa
from src/sym_crypto import encrypt_seed, decrypt_seed


def parse_arguments():
    """CMD parsing."""
    parser = argparse.ArgumentParser(description="RSA & SEED hybrid encryption")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Key generation mode')
    group.add_argument('-enc', '--encryption', action='store_true', help='Encryption mode')
    group.add_argument('-dec', '--decryption', action='store_true', help='Decryption mode')

    parser.add_argument('-c', '--config', default='settings.json', help='Path to the configuration file')


    parser.add_argument('--pub', help='Path to your public key (PEM)')
    parser.add_argument('--priv', help='Path to your private key (PEM)')
    parser.add_argument('--sym', help='Path to your encrypted symmetric key')
    parser.add_argument('--input', help='Path to the input file')
    parser.add_argument('--output', help='path to the output file')

    return parser.parse_args()


def determine_mode(args) -> str:
    """Determining the operating mode for use in a match/case."""
    if args.generation: return 'generation'
    if args.encryption: return 'encryption'
    if args.decryption: return 'decryption'
    return 'unknown'


def main():
    try:
        args = parse_arguments()

        settings = load_json(args.config)

        files = settings.get('files', {})
        params = settings.get('crypto_params', {})

        pub_key_path = args.pub if args.pub else files.get('public_key')
        priv_key_path = args.priv if args.priv else files.get('secret_key')
        sym_key_path = args.sym if args.sym else files.get('symmetric_key')

        mode = determine_mode(args)

        match mode:
            case 'generation':
                print("\n!!STARTING KEY GENERATION!!")
                print("--Generating a symmetric SEED key...")
                sym_key = os.urandom(params.get('seed_key_size', 16))

                print("--Generating an RSA key pair...")
                pub_bytes, priv_bytes = generate_rsa_keys(
                    public_exponent=params.get('rsa_public_exponent', 65537),
                    key_size=params.get('rsa_key_size', 2048)
                )

                print(f"--Saving the public key in {pub_key_path}...")
                write_file(pub_key_path, pub_bytes)

                print(f"--Saving the private key in {priv_key_path}...")
                write_file(priv_key_path, priv_bytes)

                print(f"--Symmetric key encryption and storage in {sym_key_path}...")
                encrypted_sym_key = encrypt_rsa(pub_bytes, sym_key)
                write_file(sym_key_path, encrypted_sym_key)

                print("-Key generation has been completed successfully!")

            case 'encryption':
                input_file = args.input if args.input else files.get('initial_file')
                output_file = args.output if args.output else files.get('encrypted_file')

                print("\n!!STARTING DATA ENCRYPTION!!")
                print(f"--Loading the RSA private key from {priv_key_path}...")
                priv_key_pem = read_file(priv_key_path)

                print(f"--Reading and decrypting the symmetric SEED key from {sym_key_path}...")
                enc_sym_key = read_file(sym_key_path)
                sym_key = decrypt_rsa(priv_key_pem, enc_sym_key)

                print(f"--Reading the source file {input_file}...")
                plain_text = read_file(input_file)

                print("--Data encryption using the SEED algorithm...")
                iv, cipher_text = encrypt_seed(plain_text, sym_key, params.get('seed_block_size', 128))

                print(f"--Saving encrypted file in {output_file}...")
                write_file(output_file, iv + cipher_text)

                print("-The encryption has been successfully completed!")

            case 'decryption':
                input_file = args.input if args.input else files.get('encrypted_file')
                output_file = args.output if args.output else files.get('decrypted_file')

                print("\n!!STARTING DATA DECRYPTION!!")
                print(f"--Loading the RSA private key from {priv_key_path}...")
                priv_key_pem = read_file(priv_key_path)

                print(f"--Reading and decrypting the symmetric SEED key from {sym_key_path}...")
                enc_sym_key = read_file(sym_key_path)
                sym_key = decrypt_rsa(priv_key_pem, enc_sym_key)

                print(f"--Reading encrypted file {input_file}...")
                file_content = read_file(input_file)

                if len(file_content) < 16:
                    raise ValueError("The file content is too short (missing IV).")

                iv = file_content[:16]
                cipher_text = file_content[16:]

                print("--Decryption of data by the SEED algorithm...")
                plain_text = decrypt_seed(cipher_text, sym_key, iv, params.get('seed_block_size', 128))

                print(f"--Saving the result in {output_file}...")
                write_file(output_file, plain_text)

                print("-Decryption has been completed successfully!")

            case _:
                print("!!!Error: Unknown operating mode.")

    except IOError as e:
        print(f"!!! Input/Output error: {e}")
    except ValueError as e:
        print(f"!!! Data error: {e}")
    except RuntimeError as e:
        print(f"!!! Cryptographic error: {e}")
    except Exception as e:
        print(f"!!! Unexpected error: {e}")


if __name__ == '__main__':
    main()