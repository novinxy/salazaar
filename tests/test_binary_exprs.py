from salazaar import translate_code


def test_equality_compare(multiline):
    # Arrange
    js_code = """
    var1 == var2;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 == var2
    """

    assert py_code == multiline(expected_py)


def test_not_equal_compare(multiline):
    # Arrange
    js_code = """
    var1 != var2;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 != var2
    """

    assert py_code == multiline(expected_py)


def test_greater_compare(multiline):
    # Arrange
    js_code = """
    var1 > var2;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 > var2
    """

    assert py_code == multiline(expected_py)


def test_greater_or_equal_compare(multiline):
    # Arrange
    js_code = """
    var1 >= var2;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 >= var2
    """

    assert py_code == multiline(expected_py)


def test_less_compare(multiline):
    # Arrange
    js_code = """
    var1 < var2;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 < var2
    """

    assert py_code == multiline(expected_py)


def test_less_or_equal_compare(multiline):
    # Arrange
    js_code = """
    var1 <= var2;
    """

    # Act
    py_code = translate_code(js_code)

    # Assert
    expected_py = """
    var1 <= var2
    """

    assert py_code == multiline(expected_py)
