import json2py


def test_simple_wile_loop(multiline):
    # arrange
    js_code = """
    while (true) {
        var i = 10;
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
    while True:
        i = 10
    """
    assert result == multiline(expected_py)


def test_for_in_loop(multiline):
    # arrange
    js_code = """
    for (const i in collection) {
        var tmp = collection[i];
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
    for i in range(len(collection)):
        tmp = collection[i]
    """
    assert result == multiline(expected_py)


def test_for_of_loop(multiline):
    # arrange
    js_code = """
    for (const elem of  collection) {
        var tmp = elem;
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
    for elem in collection:
        tmp = elem
    """
    assert result == multiline(expected_py)

