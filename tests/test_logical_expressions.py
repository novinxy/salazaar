
import esprima
import pytest

from salazaar import salazaar


expressions = [
    '!false && true || !true',
    '!temp',
    '(false && true) && true',
    'false && (true || true)',
    'false && true && true',
    'false && true || false && true || true',
    'false && true || true',
    'false || !true && false || false',
    'false || true && false || true && false || true',
    'false || true && true',
    'var1 && (var2 && var3)',
    'var1 == var2 && i == 10',
    'var1 == var2 && var3 != var4 || var5 == var6',
    'var1 == var2 || i == 10',
]


@pytest.mark.parametrize("js", expressions)
def test_logical_expressions(js):
    js_ast = esprima.parseScript(js)
    
    py_code = salazaar.translate_code(js)
    
    js_back = py_code.replace('False', 'false').replace('True', 'true').replace('and', '&&').replace('or', '||').replace('not', '!')
    js_back_ast = esprima.parseScript(js_back)
    assert js_back_ast.toDict() == js_ast.toDict()
