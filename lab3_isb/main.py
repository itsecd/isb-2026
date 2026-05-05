import argparse
import scenario1
import scenario2
import scenario3



def argparsing() -> argparse.Namespace:
    """
    Парсер аргументов командной строки.
    :return: объект с аргументами командной строки
    """

    parser = argparse.ArgumentParser(description="Hybrid cryptosystem")
    subparsers = parser.add_subparsers(dest="scenario", required=True)

    gen_parser = subparsers.add_parser("gen", help="Generate keys")
    gen_parser.add_argument("--ENC_PATH", type=str, required=True)
    gen_parser.add_argument("--OPN_KEY_PATH", type=str, required=True)
    gen_parser.add_argument("--PRV_KEY_PATH", type=str, required=True)
    gen_parser.add_argument("--SIZE", type=int, required=True)

    enc_parser = subparsers.add_parser("enc", help="Encrypt file")
    enc_parser.add_argument("--TXT_PATH", type=str, required=True)
    enc_parser.add_argument("--PRV_ASYM_KEY_PATH", type=str, required=True)
    enc_parser.add_argument("--ENC_KEY_PATH", type=str, required=True)
    enc_parser.add_argument("--ENC_TXT_PATH", type=str, required=True)

    dec_parser = subparsers.add_parser("dec", help="Decrypt file")
    dec_parser.add_argument("--ENC_TXT_PATH", type=str, required=True)
    dec_parser.add_argument("--PRV_ASYM_KEY_PATH", type=str, required=True)
    dec_parser.add_argument("--ENC_KEY_PATH", type=str, required=True)
    dec_parser.add_argument("--DEC_TXT_PATH", type=str, required=True)

    return parser.parse_args()

   

def main():
    args = argparsing()
    if args.scenario == "gen":
        scenario1.run_scenario1(args.ENC_PATH, args.OPN_KEY_PATH, args.PRV_KEY_PATH, args.SIZE)
    elif args.scenario == "enc":
        scenario2.run_scenario2(args.TXT_PATH, args.PRV_ASYM_KEY_PATH, args.ENC_KEY_PATH, args.ENC_TXT_PATH)
    elif args.scenario == "dec":
        scenario3.run_scenario3(args.ENC_TXT_PATH, args.PRV_ASYM_KEY_PATH, args.ENC_KEY_PATH, args.DEC_TXT_PATH)

if __name__ == "__main__":
    main()
