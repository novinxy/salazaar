import pytest

import salazaar
from tests.conftest import CodeTranspile, translate_and_compare


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
        CodeTranspile(
            id="decimal",
            js="var number = 10;",
            py="number = 10",
        ),
        CodeTranspile(
            id="float",
            js="var number = 1.5;",
            py="number = 1.5",
        ),
        CodeTranspile(
            id="boolean true",
            js="var flag = true",
            py="flag = True",
        ),
        CodeTranspile(
            id="boolean false",
            js="var flag = false",
            py="flag = False",
        ),
        CodeTranspile(
            id="string",
            js="var text = 'Hello world';",
            py="text = 'Hello world'",
        ),
        CodeTranspile(
            id="list",
            js="var collection = [1, 2, 3]",
            py="collection = [1, 2, 3]",
        ),
        CodeTranspile(
            id="list of variables",
            js="var collection = [var1, var2, var3];",
            py="collection = [var1, var2, var3]",
        ),
        CodeTranspile(
            id="objects",
            js="var collection = {'key1': 'value1', 'key2': 'value2'};",
            py="collection = {'key1': 'value1', 'key2': 'value2'}",
        ),
        CodeTranspile(
            id="list of objects",
            js="var collection = [{'key1': '1st', 'key2': 2}, {'key3': true, 'key4': [1, 2, 3]}];",
            py="collection = [{'key1': '1st', 'key2': 2}, {'key3': True, 'key4': [1, 2, 3]}]",
        ),
        CodeTranspile(
            id="multiple - tuple unpack",
            js="var [number, flag] = [10, true]",
            py="number, flag = (10, True)",
        ),
        CodeTranspile(
            id="multiple - split with comma",
            js="let x = 20, y = 30, z = 40;",
            py="""
                x = 20
                y = 30
                z = 40
            """,
        ),
        CodeTranspile(
            id="multiple - assignment",
            js="let x = y = z = 10",
            py="x = y = z = 10",
        ),
        CodeTranspile(
            id="multiple - declaration then assignment",
            js="""
                let x = y = z;
                nx = y = z = 10;
            """,
            py="x = y = z = ",
        ),
        CodeTranspile(
            id="assignment expression",
            js="flag = true",
            py="flag = True",
        ),
        CodeTranspile(
            id="declaration - undefined",
            js="let nothing",
            py="nothing = None",
        ),
    ],
    ids=CodeTranspile.get_pytest_id,
)
def test_variable_declaration(p: CodeTranspile):
    translate_and_compare(p.js, p.py)
