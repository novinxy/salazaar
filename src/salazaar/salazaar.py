import esprima

from salazaar.ast_converter import ASTConverter
from salazaar.parser import Parser


def translate(js_code: str) -> str:
    module = esprima.parseModule(js_code, options={"comment": True, "attachComment": True})

    js_ast = module.toDict()

    py_ast = ASTConverter().visit(js_ast)

    parser = Parser()

    return parser.unparse(py_ast)
