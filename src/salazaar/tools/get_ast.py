import argparse
import ast
import json
import sys
from typing import TextIO

import salazaar


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

    parser.add_argument("--lang", type=str, choices=["py", "js"], default="js")

    args = parser.parse_args()

    if args.input:
        code = args.input
    else:
        input: TextIO = args.input_file

        code = input.read()

    if args.lang == "py":
        tree = ast.parse(code)
        ast_string = ast.dump(tree, indent=2)
    else:
        ast_string = salazaar.salazaar.get_js_ast(code)
        ast_string = json.dumps(ast_string, indent=2)

    print(ast_string)



if __name__ == "__main__":
    main()
