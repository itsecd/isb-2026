import argparse
from pathlib import Path
from collections import Counter

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", help="ciphertext file")
    p.add_argument("--out", dest="out_path", help="output freqs.txt")
    p.add_argument("--top", type=int, help="top symbols to print/write")
    args = p.parse_args()

    text = Path(args.in_path).read_text(encoding="utf-8").replace("\r", "")
    cnt = Counter(ch for ch in text if ch != "\n")
    total = sum(cnt.values())

    lines = []
    lines.append(f"Total chars (no newlines): {total}")
    lines.append(f"Unique symbols: {len(cnt)}")
    lines.append("")
    lines.append("Top frequency symbols:")
    for ch, c in cnt.most_common(args.top):
        show = "<SPACE>" if ch == " " else ("\\t" if ch == "\t" else ch)
        freq = c / total if total else 0
        lines.append(f"{show!r:10} : {c:5d}  ({freq:.6f})")

    Path(args.out_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"OK: wrote freqs to {args.out_path}")

if __name__ == "__main__":
    main()