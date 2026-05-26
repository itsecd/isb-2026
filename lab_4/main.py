"""
Command-line interface for the file integrity checker.
"""

import argparse
import sys

from hash_utils import sha256_file, save_checksum, verify_file, write_verification_result, collision_demo


def create_parser():
    """
    Build and return the command-line parser.

    Returns:
        argparse.ArgumentParser: Configured parser.
    """
    parser = argparse.ArgumentParser(description="SHA-256 file integrity checker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("hash", help="Compute SHA-256")
    p1.add_argument("file", help="Path to file")

    p2 = sub.add_parser("save", help="Save checksum")
    p2.add_argument("file", help="Path to file")
    p2.add_argument("-o", "--output", default=None, help="Checksum output path")

    p3 = sub.add_parser("verify", help="Verify file")
    p3.add_argument("file", help="Path to file")
    p3.add_argument("-c", "--checksum", default=None, help="Checksum file path")
    p3.add_argument("-r", "--result", default="verify_result.txt", help="Result file path")

    p4 = sub.add_parser("collide", help="Collision demo")
    p4.add_argument("-n", "--attempts", type=int, default=10000, help="Maximum attempts")
    p4.add_argument("-p", "--prefix-len", type=int, default=8, help="Prefix length")

    return parser


def main(argv=None):
    """
    Run the selected command.

    Args:
        argv (list[str] | None): Optional CLI arguments for testing.

    Returns:
        int: Exit code.
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        if args.cmd == "hash":
            print(sha256_file(args.file))

        elif args.cmd == "save":
            checksum = sha256_file(args.file)
            checksum_path = save_checksum(args.file, checksum, args.output)
            print(f"Saved: {checksum_path}")
            print(checksum)

        elif args.cmd == "verify":
            ok, current, saved = verify_file(args.file, args.checksum)
            print(f"Current: {current}")
            print(f"Saved:   {saved}")
            print("OK" if ok else "FAILED")
            result_path = write_verification_result(ok, current, saved, args.result)
            print(f"Result saved: {result_path}")

        elif args.cmd == "collide":
            result = collision_demo(args.attempts, args.prefix_len)
            if result["found"]:
                print("COLLISION FOUND")
                print(f"Attempts: {result['attempts']}")
                print(f"Hash: {result['hash']}")
                print(f"Message 1: {result['first']}")
                print(f"Message 2: {result['second']}")
            else:
                print(f"No collision after {result['attempts']} attempts")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())