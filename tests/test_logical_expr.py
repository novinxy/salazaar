from json2py import translate_code


def test_logical_and(multiline):
    # Arrange
    js_code = """
    var1 == var2 && i == 10;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 == var2 and i == 10
    """

    assert py_code == multiline(expected_py)


def test_logical_or(multiline):
    # Arrange
    js_code = """
    var1 == var2 || i == 10;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 == var2 or i == 10
    """

    assert py_code == multiline(expected_py)


def test_complex_logical(multiline):
    # Arrange
    js_code = """
    var1 == var2 || i == 10 && str1 == 'HELLO';
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 == var2 or i == 10 and str1 == 'HELLO'
    """

    assert py_code == multiline(expected_py)

