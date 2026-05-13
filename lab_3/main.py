import sys
from file_utils import load_settings
from modules import parse_args
from modules import generate_mode, encrypt_mode, decrypt_mode, merge_args_with_settings


def main() -> None:
    try:
        args = parse_args()

        # Handle potential configuration loading errors
        try:
            settings = load_settings(args.config)
            args = merge_args_with_settings(args, settings)
        except FileNotFoundError:
            # If the config file isn't found, we can proceed with CLI args only
            pass
        except Exception as e:
            print(f"Configuration error: {e}")

        match args.mode:
            case "gen":
                generate_mode(args)
            case "enc":
                encrypt_mode(args)
            case "dec":
                decrypt_mode(args)

    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()