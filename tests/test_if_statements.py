import json2py


def test_simple_if(multiline):
    # arrange
    js_code = """
    if (false) {
        var tmp = 10;
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
    if False:
        tmp = 10
    """
    assert result == multiline(expected_py)


def test_else(multiline):
    # arrange
    js_code = """
    if (false) {
        var tmp = 10;
    } else {
        var tmp = 20;
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
    if False:
        tmp = 10
    else:
        tmp = 20
    """
    assert result == multiline(expected_py)
    

def test_ifelse(multiline):
    # arrange
    js_code = """
    if (false) {
        var tmp = 10;
    } else if (i == 10) {
        var tmp = 20;
    }
    """

    # act
    result = json2py.translate_code(js_code)

    # assert
    expected_py = """
    if False:
        tmp = 10
    elif i == 10:
        tmp = 20
    """
    assert result == multiline(expected_py)
