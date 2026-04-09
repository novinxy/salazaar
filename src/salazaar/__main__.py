import argparse
import sys
from contextlib import nullcontext

from salazaar import salazaar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        nargs="?",
        help="Input file or '-' for stdin (default: stdin)",
    )

    args = parser.parse_args()

    if args.input in (None, "-"):
        stream_cm = nullcontext(sys.stdin)
    else:
        stream_cm = open(args.input, "r")

    with stream_cm as f:
        content = f.read()

        data_str = salazaar.translate_code(content)

        print(data_str)


if __name__ == "__main__":
    main()
