import pytest

import salazaar
from tests.conftest import CodeTranspile


def test_given_different_javascript_declaration_types_return_same_declaration():
    # arrange
    var_declaration = "var number = 10;"
    let_declaration = "let number = 10;"
    const_declaration = "const number = 10;"
    expected_py = "number = 10"

    # act
    var_result = salazaar.translate_code(var_declaration)
    let_result = salazaar.translate_code(let_declaration)
    const_result = salazaar.translate_code(const_declaration)

    # assert
    assert expected_py == var_result == let_result == const_result


@pytest.mark.parametrize(
    "p",
    [
        CodeTranspile(js="var number = 10;", py="number = 10", id="decimal"),
        CodeTranspile(js="var number = 1.5;", py="number = 1.5", id="float"),
        CodeTranspile(js="var flag = true", py="flag = True", id="boolean true"),
        CodeTranspile(js="var flag = false", py="flag = False", id="boolean false"),
        CodeTranspile(js="var text = 'Hello world';", py="text = 'Hello world'", id="string"),
        CodeTranspile(js="var collection = [1, 2, 3]", py="collection = [1, 2, 3]", id="list"),
        CodeTranspile(
            js="var collection = [var1, var2, var3];", py="collection = [var1, var2, var3]", id="list of variables"
        ),
        CodeTranspile(
            js="var collection = {'key1': 'value1', 'key2': 'value2'};",
            py="collection = {'key1': 'value1', 'key2': 'value2'}",
            id="objects",
        ),
        CodeTranspile(
            js="var collection = [{'key1': 'value1', 'key2': 'value2'}, {'key3': 'value3', 'key4': 'value4'}];",
            py="collection = [{'key1': 'value1', 'key2': 'value2'}, {'key3': 'value3', 'key4': 'value4'}]",
            id="list of objects",
        ),
        CodeTranspile(
            js="var [number, flag] = [10, true]",
            py="number, flag = (10, True)",
            id="multiple - tuple unpack",
        ),
        CodeTranspile(
            js="let x = 20, y = 30, z = 40;",
            py="x = 20\ny = 30\nz = 40",
            id="multiple - split with comma",
        ),
        CodeTranspile(
            js="let x = y = z = 10",
            py="x = y = z = 10",
            id="multiple - assignment",
        ),
        CodeTranspile(
            js="flag = true",
            py="flag = true",
            id="assignment expression",
        ),
        CodeTranspile(
            js="let nothing",
            py="nothing = None",
            id="declaration - undefined",
        ),
    ],
    ids=CodeTranspile.get_pytest_id,
)
def test_variable_declaration(p: CodeTranspile):
    result = salazaar.translate_code(p.js)

    assert result == p.py
