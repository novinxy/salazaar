import argparse
import ast
import os

import esprima

from salazaar.ast_converter import ASTConverter


def get_js_ast(js_code: str) -> dict:
    data = esprima.parse(js_code)
    return data.toDict()


def translate_code(js_code: str) -> str:
    js_ast = get_js_ast(js_code)

    py_ast = ASTConverter().visit(js_ast)
    return ast.unparse(ast.fix_missing_locations(py_ast))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="temp.js", required=True)
    parser.add_argument("--output", default="temp.py", required=True)
    args = parser.parse_args()

    input_file_name = args.input
    output_file_name = args.output

    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"Input file '{input_file_name}' does not exist.")

    with open(input_file_name, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    data_str = translate_code(content)

    os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
    with open(output_file_name, "w+", encoding="utf-8") as f:
        f.write(data_str)


if __name__ == "__main__":
    main()
