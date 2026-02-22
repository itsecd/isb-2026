import argparse
from pathlib import Path
from collections import Counter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_path", type = str, help="ciphertext file")
    parser.add_argument("--top", type=int, default=25)
    args = parser.parse_args()

    text = Path(args.in_path).read_text(encoding="utf-8")
    text = text.replace("\n", " ").replace("\r", "")

    cnt = Counter(text)
    print(f"Total chars (no newlines): {len(text)}")
    print(f"Unique symbols: {len(cnt)}")
    print("\n Top frequency symbols:")
    for ch,c in cnt.most_common(args.top):
        show = "<SPACE>" if ch == " " else("TAB" if ch == "\t" else ch)
        print(f"{show!r:10} : {c}")

if __name__ == "__main__":
    main()