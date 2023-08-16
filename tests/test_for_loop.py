import json2py


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


def test_for_loop_ascending(multiline):
    # arrange
    js_code = """
    for (let index = 0; index < array.length; index++) {
        const element = array[index];
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
   for index in range(len(array)):
        element = array[index]
    """
    assert result == multiline(expected_py)


def test_for_loop_descending(multiline):
    # arrange
    js_code = """
    for (let index = array.length - 1; index >= 0; index--) {
        const element = array[index];
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
   for index in range(len(arr) -1, -1, -1):
        element = array[index]
    """
    assert result == multiline(expected_py)
