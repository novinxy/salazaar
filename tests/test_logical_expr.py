import itertools
from salazaar import translate_code
import pytest


translations = [
    (
        'var1 == var2 && i == 10;',
        'var1 == var2 and i == 10'
    ),
    (
        'var1 == var2 || i == 10;',
        'var1 == var2 or i == 10'
    ),
    (
        "var1 == var2 && (i == 10 && str1 == 'HELLO') || j > 5 && z != true;",
        "var1 == var2 and (i == 10 and str1 == 'HELLO') or j > 5 and z != True"
    ),
    (
        "(true || false) && (false || true) && (true || true) && (false || false);",
        "(True or False) and (False or True) and (True or True) and (False or False)"
    ),
    (
        "false && (true || true);",
        "False and (True or True)"
    ),
    (
        "false && true || true;",
        "False and True or True"
    ),
    (
        "false || true && true;",
        "False or True and True"
    ),
    (
        "false || true && false;",
        "False or True and False"
    ),
    (
        "false && true && true;",
        "False and True and True"
    ),
]


@pytest.mark.parametrize('js,py', translations)
def test_same_string(multiline, js, py):
    # Arrange
    py_code = translate_code(js)

    # Assert
    assert py_code == multiline(py)


@pytest.mark.parametrize('js,py', translations)
def test_eval(multiline, js, py):
    # Act
    py_code = translate_code(js)

    numbers = list(range(5, 15))

    variables = list(itertools.product(numbers,numbers,numbers, ['Hello', 'WORLD'], numbers, [True, False]))

    # Assert
    for vars in variables:
        vars_dict = {
            'var1': vars[0],
            'var2': vars[1],
            'i': vars[2],
            'str1': vars[3],
            'j': vars[4],
            'z': vars[5],
        }
        assert eval(py_code, vars_dict) == eval(multiline(py), vars_dict)
