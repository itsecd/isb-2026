import sys
import argparse
from file_utils import *
from symmetric import *
from asymmetric import *
from modules import *


def main() -> None:
    args = parse_args()
    settings = load_settings(args.config)
    args = merge_args_with_settings(args, settings)

    match args.mode:
        case("gen"):
            generate_mode(args)
        case("enc"):
            encrypt_mode(args)
        case("dec"):
            decrypt_mode(args)


if __name__ == "__main__":
    main ()