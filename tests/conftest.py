import glob
import shutil
import textwrap
import os


def test_function_template(test_name: str, js: str, py: str) -> str:
    js = js.replace('\\', '\\\\')
    py = py.replace('\\', '\\\\')

    return f'''

def test_{test_name}():
    # Arrange
    js = """
{js}
""".strip()

    py = """
{py}
""".strip()

    # Act
    result = salazaar.translate_code(js)

    # Assert
    assert result.strip() == py.strip(), f"Expected: {{py}}, but got: {{result}}"
'''


def generate_test_functions(markdown: str):

    test_cases = markdown.split('## Test case:')[1:]

    tests = []
    for test_case in test_cases:
        test_case_name = test_case.split('\n')[0].strip()
        test_case_name = test_case_name.replace(' ', '_').replace('-', '_').replace('___', '_').replace('__', '_')

        tests.append((
            test_case_name,
            test_case.split('```js')[1].split('```')[0].strip(),
            test_case.split('```py')[1].split('```')[0].strip()
        ))

    result = "import salazaar"

    for name, js, py in tests:
        js = textwrap.dedent(js).strip()
        py = textwrap.dedent(py).strip()

        test_function = test_function_template(name, js, py)

        result += test_function

    return result


def clean_generated_tests():
    shutil.rmtree('tests/generated', ignore_errors=True)
    os.makedirs('tests/generated', exist_ok=True)

    with open('tests/generated/__init__.py', mode='w+', encoding='utf-8', errors='ignore'):
        pass


def generate_test_files():
    markdown_files = glob.glob("tests/markdown/*.md")

    for markdown_file in markdown_files:
        result_file = 'tests/generated/test_' + os.path.basename(markdown_file).split('.')[0] + ".py"

        with open(markdown_file, mode='r', encoding='utf-8') as file:
            content = file.read()

        test_file_content = generate_test_functions(content)
        with open(result_file, mode='w+', encoding='utf-8', errors='ignore') as file:
            file.write(test_file_content)


def generate_markdown_tests():
    clean_generated_tests()

    generate_test_files()


def pytest_configure():
    generate_markdown_tests()
