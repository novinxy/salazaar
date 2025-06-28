import salazaar


def test_simple_if(multiline):
    # arrange
    js_code = """
    if (false) {
        var tmp = 10;
    }
    """

    # act
    result = salazaar.translate_code(js_code)

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
    result = salazaar.translate_code(js_code)

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
    result = salazaar.translate_code(js_code)

    # assert
    expected_py = """
    if False:
        tmp = 10
    elif i == 10:
        tmp = 20
    """
    assert result == multiline(expected_py)
    

def test_multiple_elif_plus_else(multiline):
    # arrange
    js_code = """
    if (false) {
        var tmp = 10;
    } else if (i == 10) {
        var tmp = 20;
    } else if (i == -1) {
        var tmp = 1;
    } else if (i == 50) {
        var tmp = 100;
    } else {
        var tmp = 5000;
    }
    """

    # act
    result = salazaar.translate_code(js_code)

    # assert
    expected_py = """
    if False:
        tmp = 10
    elif i == 10:
        tmp = 20
    elif i == -1:
        tmp = 1
    elif i == 50:
        tmp = 100
    else:
        tmp = 5000
    """
    assert result == multiline(expected_py)
    
