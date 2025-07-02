import ast
import sys
import argparse
from typing import TextIO


def main():
    parser = argparse.ArgumentParser(description="Get AST of a JavaScript code snippet")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--input_file",
        type=argparse.FileType("r"),
        required=False,
        help="Input JavaScript code file",
        default=sys.stdin,
    )
    group.add_argument("--input", type=str, required=False, help="Input JavaScript code file")

    args = parser.parse_args()

    if args.input:
        code = args.input
    else:
        input: TextIO = args.input_file

        code = input.read()
    tree = ast.parse(code)
    p = ast.dump(tree, indent=2)
    print(p)


if __name__ == "__main__":
    main()
