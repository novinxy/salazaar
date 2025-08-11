import salazaar


def test_given_different_javascript_declaration_types_return_same_declaration():
    # arrange
    var_declaration = "var number = 10;"
    let_declaration = "let number = 10;"
    const_declaration = "const number = 10;"
    expected_py = "number = 10"

    # act
    var_result = salazaar.translate_code(var_declaration)
    let_result = salazaar.translate_code(let_declaration)
    const_result = salazaar.translate_code(const_declaration)

    # assert
    assert expected_py == var_result == let_result == const_result
