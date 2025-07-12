import pytest

from tests.conftest import CodeTranspile, translate_and_compare


@pytest.mark.parametrize(
    "p",
    [
        CodeTranspile(
            id="equality compare",
            js="var1 == var2;",
            py="var1 == var2",
        ),
        CodeTranspile(
            id="not equal compare",
            js="var1 != var2;",
            py="var1 != var2",
        ),
        CodeTranspile(
            id="greater compare",
            js="var1 > var2;",
            py="var1 > var2",
        ),
        CodeTranspile(
            id="greater or equal compare",
            js="var1 >= var2;",
            py="var1 >= var2",
        ),
        CodeTranspile(
            id="less compare",
            js="var1 < var2;",
            py="var1 < var2",
        ),
        CodeTranspile(
            id="less or equal compare",
            js="var1 <= var2;",
            py="var1 <= var2",
        ),
    ],
    ids=CodeTranspile.get_pytest_id,
)
def test_binary_expressions(p: CodeTranspile):
    translate_and_compare(p.js, p.py)
