import json2py


def test_declare_decimal():
    # arrange
    js_code = "var number = 10;"

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = "number = 10"
    assert result == expected_py


def test_declare_float():
    # arrange
    js_code = "var number = 1.5;"

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = "number = 1.5"
    assert result == expected_py


def test_declare_boolean():
    # arrange
    js_code = "var flag = true;"

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = "flag = True"
    assert result == expected_py


def test_declare_string():
    # arrange
    js_code = "var text = 'Hello world';"

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = "text = 'Hello world'"
    assert result == expected_py


def test_declare_simple_list():
    # arrange
    js_code = "var collection = [1, 2, 3];"

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = "collection = [1, 2, 3]"
    assert result == expected_py


def test_declare_list_of_variables():
    # arrange
    js_code = "var collection = [var1, var2, var3];"

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = "collection = [var1, var2, var3]"
    assert result == expected_py


def test_declare_objects():
    # arrange
    js_code = "var collection = {'key1': 'value1', 'key2': 'value2'};"

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = "collection = {'key1': 'value1', 'key2': 'value2'}"
    assert result == expected_py
