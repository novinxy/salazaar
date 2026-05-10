import esprima

from salazaar.js_converter import JsConverter
from salazaar.parser import Parser


def translate(js_code: str, unsafe_fixes: bool = False) -> str:
    module = esprima.parseModule(js_code, options={"comment": True, "attachComment": True})

    js_ast = module.toDict()

    py_ast = JsConverter(unsafe_fixes=unsafe_fixes).visit(js_ast)

    parser = Parser()

    return parser.unparse(py_ast)
