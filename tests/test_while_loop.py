import salazaar.json2py as json2py


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
