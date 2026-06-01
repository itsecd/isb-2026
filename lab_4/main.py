import sys
from cli import run_cli
from gui import run_gui

def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()