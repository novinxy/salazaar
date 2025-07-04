import salazaar


def test_simple_wile_loop(multiline):
    # arrange
    js_code = """
    while (true) {
        var i = 10;
    }
    """

    # act
    result = salazaar.translate_code(js_code)

    # assert
    expected_py = """
    while True:
        i = 10
    """
    assert result == multiline(expected_py)
