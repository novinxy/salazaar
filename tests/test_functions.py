import salazaar


def test_simple_function(multiline):
    # arrange
    js_code = """
    function Test() {
        var tmp = 10;
    }
    """

    # act
    result = salazaar.translate_code(js_code)

    # assert
    expected_py = """
    def Test():
        tmp = 10
    """
    assert result == multiline(expected_py)


def test_function_with_argument(multiline):
    # arrange
    js_code = """
    function Test(arg1) {
        var tmp = 10;
    }
    """

    # act
    result = salazaar.translate_code(js_code)

    # assert
    expected_py = """
    def Test(arg1):
        tmp = 10
    """
    assert result == multiline(expected_py)


def test_function_with_multiple_arguments(multiline):
    # arrange
    js_code = """
    function Test(arg1, arg2, arg3) {
        var tmp = 10;
    }
    """

    # act
    result = salazaar.translate_code(js_code)

    # assert
    expected_py = """
    def Test(arg1, arg2, arg3):
        tmp = 10
    """
    assert result == multiline(expected_py)
