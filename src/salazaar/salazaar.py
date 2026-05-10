import esprima

from salazaar.js_converter import JsConverter
from salazaar.parser import Parser


def translate(js_code: str, unsafe_fixes: bool = False, comments: bool = False) -> str:
    """Translates JavaScript to Python code

    Args:
        js_code (str): JavaScript code to translate
        unsafe_fixes (bool, optional): Enables JavaScript built-in utilities translation. Defaults to False.
        comments (bool, optional): Enables leading comments translation. Defaults to False.

    Returns:
        str: Python code equivalent to the provided JavaScript code
    """
    module = esprima.parseModule(js_code, options={"comment": True, "attachComment": True})

    js_ast = module.toDict()

    py_ast = JsConverter(
        unsafe_fixes=unsafe_fixes,
        comments=comments,
    ).visit(js_ast)

    parser = Parser()

    return parser.unparse(py_ast)
