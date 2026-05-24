import argparse
import sys
import time

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

from hash_core import (
    run_single_experiment,
    run_experiments,
    summarize_results,
    compute_hash,
)


_USE_COLOR = True

def _c(code: str, text: str) -> str:
    if not _USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"

GREEN  = lambda t: _c("92", t)
YELLOW = lambda t: _c("93", t)
CYAN   = lambda t: _c("96", t)
BOLD   = lambda t: _c("1",  t)
RED    = lambda t: _c("91", t)
DIM    = lambda t: _c("2",  t)




def print_banner():
    banner = r"""   
  Лабораторная №4 · Лавинный эффект хеш-функций
"""
    print(CYAN(banner))


def print_hash_pair(label: str, original: str, modified: str,
                    h_orig: str, h_mod: str, diff_pct: float, bits: int):
    print(f"  {BOLD(label)}")
    print(f"    Исходный текст : {DIM(repr(original))}")
    print(f"    Изменённый     : {YELLOW(repr(modified))}")
    print(f"    SHA-256 до     : {DIM(h_orig[:32])}…")
    print(f"    SHA-256 после  : {YELLOW(h_mod[:32])}…")

    bar_len = 40
    filled = int(bar_len * diff_pct / 100)
    bar = GREEN("█" * filled) + DIM("░" * (bar_len - filled))
    color = GREEN if diff_pct >= 45 else YELLOW if diff_pct >= 25 else RED
    print(f"    Различий бит   : [{bar}] {color(f'{diff_pct:.1f}%')} ({bits} / 256)")
    print()


def print_summary_table(summary: dict, algorithm: str):
    print(BOLD("\n  ╔══════════════════════════════════════════╗"))
    print(BOLD("  ║         СВОДНАЯ СТАТИСТИКА               ║"))
    print(BOLD("  ╚══════════════════════════════════════════╝"))
    print(f"  Алгоритм       : {CYAN(algorithm.upper())}")
    print(f"  Экспериментов  : {summary['total_experiments']}")
    print(f"  Среднее %      : {GREEN(str(summary['avg_diff_percent'])) if summary['avg_diff_percent'] >= 45 else YELLOW(str(summary['avg_diff_percent']))}")
    print(f"  Мин. %         : {summary['min_diff_percent']}")
    print(f"  Макс. %        : {summary['max_diff_percent']}")
    print(f"  Сред. бит      : {summary['avg_changed_bits']} / 256")
    print()
    print(f"  {'Тип модификации':<35} {'Ср. % различий':>15}")
    print(f"  {'─' * 52}")
    for mod, pct in summary["by_modification"].items():
        color = GREEN if pct >= 45 else YELLOW
        print(f"  {mod:<35} {color(f'{pct:>14.2f}%')}")

    quality = summary["avg_diff_percent"]
    print()
    if quality >= 45:
        verdict = GREEN("Отличный лавинный эффект (~50%)")
    elif quality >= 30:
        verdict = YELLOW("Умеренный лавинный эффект")
    else:
        verdict = RED("Слабый лавинный эффект")
    print(f"  Вывод: {verdict}")
    print()




def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lab4_cli",
        description="Исследование лавинного эффекта криптографических хеш-функций.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Примеры:
  python cli.py --text "hello world" --count 10
  python cli.py --text "пароль" --count 5 --algo md5 --mod bit
  python cli.py --text "cryptography" --count 15 --algo sha3_256 --no-color
        """,
    )
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="Исходная строка для хеширования.",
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=10,
        help="Количество экспериментов каждого типа (по умолчанию: 10).",
    )
    parser.add_argument(
        "--algo", "-a",
        choices=["sha256", "sha1", "md5", "sha3_256"],
        default="sha256",
        help="Алгоритм хеширования (по умолчанию: sha256).",
    )
    parser.add_argument(
        "--mod", "-m",
        choices=["char", "bit", "case", "all"],
        default="all",
        help="Тип модификации: char, bit, case или all (по умолчанию: all).",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Отключить ANSI-цвета в выводе.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Подробный вывод каждого эксперимента.",
    )
    return parser




def main():
    global _USE_COLOR

    parser = build_parser()
    args = parser.parse_args()

    if args.no_color:
        _USE_COLOR = False

    if args.count < 1:
        parser.error("--count должен быть >= 1")

    print_banner()

    # Исходный хеш
    h_orig = compute_hash(args.text, args.algo)
    print(f"  Исходная строка : {YELLOW(repr(args.text))}")
    print(f"  {args.algo.upper()} хеш      : {DIM(h_orig)}")
    print()

    modifications = ["char", "bit", "case"] if args.mod == "all" else [args.mod]
    total = args.count * len(modifications)

    print(BOLD(f"  Запуск {total} экспериментов…\n"))

    results = []

    if tqdm is not None:
        pbar = tqdm(
            total=total,
            desc="  Эксперименты",
            unit="эксп.",
            ncols=70,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

    def callback(current, _total):
        if tqdm is not None:
            pbar.update(1)

    try:
        for mod in modifications:
            for i in range(args.count):
                try:
                    r = run_single_experiment(args.text, mod, args.algo)
                    results.append(r)
                    if args.verbose:
                        print_hash_pair(
                            f"Эксперимент #{len(results)} ({r.modification_type})",
                            r.original_text, r.modified_text,
                            r.original_hash, r.modified_hash,
                            r.diff_percent, r.changed_bits,
                        )
                    callback(len(results), total)
                except ValueError as e:
                    sys.stderr.write(f"\n  [предупреждение] {e}\n")
    finally:
        if tqdm is not None:
            pbar.close()

    print()

    if not results:
        print(RED("  Нет результатов. Проверьте параметры."))
        sys.exit(1)

    if not args.verbose:
        print(BOLD("  Пример результата (последний эксперимент):"))
        r = results[-1]
        print_hash_pair(
            r.modification_type,
            r.original_text, r.modified_text,
            r.original_hash, r.modified_hash,
            r.diff_percent, r.changed_bits,
        )

    summary = summarize_results(results)
    print_summary_table(summary, args.algo)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Прервано пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {RED('Ошибка:')} {e}")
        sys.exit(1)
