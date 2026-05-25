# -*- coding: utf-8 -*-
"""
Name: HMACTask
Version: 0.1
Date: 25.05.2026
"""

import argparse
import sys

import modules.logger as logger
import modules.env_parser as env_parser
import modules.hmac_core as hmac_core
import modules.collision as collision

log = logger.app_logger


# ---------------------------------------------------------------------------
# CLI argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser.

    Returns:
        Configured :class:`argparse.ArgumentParser` instance.
    """
    parser = argparse.ArgumentParser(
        prog="hmactask",
        description="HMACTask — HMAC-based message authentication tool (Lab 4)",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the PyQt6 graphical interface.",
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # -- sign --
    sign_p = sub.add_parser("sign", help="Compute HMAC and save signed envelope.")
    sign_p.add_argument("message", help="Message to sign.")
    sign_p.add_argument("-k", "--key", help="Secret key (overrides .env).")
    sign_p.add_argument("-o", "--output", help="Output file path (overrides .env).")
    sign_p.add_argument(
        "-a", "--algo",
        default="sha256",
        choices=sorted(hmac_core.SUPPORTED_ALGORITHMS),
        help="Hash algorithm (default: sha256).",
    )

    # -- verify --
    verify_p = sub.add_parser("verify", help="Verify a signed envelope.")
    verify_p.add_argument("file", help="Path to the signed JSON envelope.")
    verify_p.add_argument("-k", "--key", help="Secret key (overrides .env).")

    # -- tamper --
    tamper_p = sub.add_parser("tamper", help="Test tamper detection.")
    tamper_p.add_argument("file", help="Path to the original signed envelope.")
    tamper_p.add_argument("tampered_message", help="Modified message to test.")
    tamper_p.add_argument("-k", "--key", help="Secret key (overrides .env).")

    # -- collision --
    col_p = sub.add_parser("collision", help="Run partial-collision search demo.")
    col_p.add_argument(
        "-b", "--bits",
        type=int,
        default=24,
        metavar="N",
        help="Number of leading HMAC bits that must match (default: 24).",
    )
    col_p.add_argument("-k", "--key", help="Secret key (overrides .env).")

    return parser


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def _handle_sign(args: argparse.Namespace, cfg: dict) -> None:
    """Handle the ``sign`` sub-command.

    Args:
        args: Parsed CLI arguments.
        cfg: Settings from :func:`env_parser.get_settings`.
    """
    key = args.key or cfg["secret_key"]
    output = args.output or cfg["output_file"]
    try:
        envelope = hmac_core.sign_and_save(args.message, key, output, args.algo)
        print(f"[✓] Signed envelope saved → {output}")
        print(f"    HMAC : {envelope['hmac']}")
    except Exception as exc:
        log.error("Sign failed: %s", exc)
        sys.exit(1)


def _handle_verify(args: argparse.Namespace, cfg: dict) -> None:
    """Handle the ``verify`` sub-command.

    Args:
        args: Parsed CLI arguments.
        cfg: Settings dict.
    """
    key = args.key or cfg["secret_key"]
    try:
        is_valid, envelope = hmac_core.load_and_verify(args.file, key)
        status = "[✓] VALID" if is_valid else "[✗] INVALID"
        print(f"{status} — message: {envelope['message']!r}")
        sys.exit(0 if is_valid else 2)
    except Exception as exc:
        log.error("Verify failed: %s", exc)
        sys.exit(1)


def _handle_tamper(args: argparse.Namespace, cfg: dict) -> None:
    """Handle the ``tamper`` sub-command.

    Args:
        args: Parsed CLI arguments.
        cfg: Settings dict.
    """
    key = args.key or cfg["secret_key"]
    try:
        result = hmac_core.tamper_and_verify(args.file, key, args.tampered_message)
        if result:
            print("[!] WARNING: tampered message was ACCEPTED (collision?)")
        else:
            print("[✓] Tampering detected — message correctly rejected.")
    except Exception as exc:
        log.error("Tamper check failed: %s", exc)
        sys.exit(1)


def _handle_collision(args: argparse.Namespace, cfg: dict) -> None:
    """Handle the ``collision`` sub-command.

    Args:
        args: Parsed CLI arguments.
        cfg: Settings dict.
    """
    key = args.key or cfg["secret_key"]
    collision.run_collision_demo(key, args.bits)


# ---------------------------------------------------------------------------
# Interactive menu (no sub-command given)
# ---------------------------------------------------------------------------

def _interactive_menu(cfg: dict) -> None:
    """Run an interactive text menu when no sub-command is provided.

    Args:
        cfg: Settings from :func:`env_parser.get_settings`.
    """
    while True:
        print("\n--- HMACTask Menu ---")
        print("1. Sign message  | 2. Verify envelope")
        print("3. Tamper check  | 4. Collision demo  | 0. Exit")
        choice = input(">_< ").strip()

        match choice:
            case "1":
                msg = input("Message: ").strip()
                key = input(f"Key [{cfg['secret_key']}]: ").strip() or cfg["secret_key"]
                out = input(f"Output [{cfg['output_file']}]: ").strip() or cfg["output_file"]
                try:
                    env = hmac_core.sign_and_save(msg, key, out)
                    print(f"HMAC: {env['hmac']}")
                except Exception as exc:
                    log.error(exc)

            case "2":
                path = input(f"Envelope [{cfg['output_file']}]: ").strip() or cfg["output_file"]
                key = input(f"Key [{cfg['secret_key']}]: ").strip() or cfg["secret_key"]
                try:
                    ok, env = hmac_core.load_and_verify(path, key)
                    print("[✓] VALID" if ok else "[✗] INVALID")
                except Exception as exc:
                    log.error(exc)

            case "3":
                path = input(f"Envelope [{cfg['output_file']}]: ").strip() or cfg["output_file"]
                key = input(f"Key [{cfg['secret_key']}]: ").strip() or cfg["secret_key"]
                tampered = input("Tampered message: ").strip()
                try:
                    result = hmac_core.tamper_and_verify(path, key, tampered)
                    print("[!] Accepted" if result else "[✓] Detected")
                except Exception as exc:
                    log.error(exc)

            case "4":
                key = input(f"Key [{cfg['secret_key']}]: ").strip() or cfg["secret_key"]
                bits_raw = input("Prefix bits [24]: ").strip()
                bits = int(bits_raw) if bits_raw.isdigit() else 24
                collision.run_collision_demo(key, bits)

            case "0":
                log.info("Shutting down...")
                break

            case _:
                print("Wrong arg")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    log.info("App start")
    cfg = env_parser.get_settings()
    parser = _build_parser()
    args = parser.parse_args()

    if args.gui:
        try:
            from modules.gui import run_gui
            run_gui()
        except ImportError as exc:
            log.error("PyQt6 is not installed: %s", exc)
            sys.exit(1)
    elif args.command == "sign":
        _handle_sign(args, cfg)
    elif args.command == "verify":
        _handle_verify(args, cfg)
    elif args.command == "tamper":
        _handle_tamper(args, cfg)
    elif args.command == "collision":
        _handle_collision(args, cfg)
    else:
        _interactive_menu(cfg)
