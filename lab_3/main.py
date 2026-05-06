from file_utils import load_settings
from modules import parse_args
from modules import generate_mode, encrypt_mode, decrypt_mode, merge_args_with_settings


def main() -> None:
    args = parse_args()
    settings = load_settings(args.config)
    args = merge_args_with_settings(args, settings)

    match args.mode:
        case "gen":
            generate_mode(args)
        case "enc":
            encrypt_mode(args)
        case "dec":
            decrypt_mode(args)


if __name__ == "__main__":
    main ()