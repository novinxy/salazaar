import esprima

from salazaar.ast_converter import ASTConverter
from salazaar.parser import Parser


def get_js_ast(js_code: str) -> dict:
    data = esprima.parseModule(js_code, options={"comment": True, "attachComment": True})
    return data.toDict()


def translate_code(js_code: str) -> str:
    js_ast = get_js_ast(js_code)

    py_ast = ASTConverter().visit(js_ast)

    parser = Parser()

    return parser.unparse(py_ast)
