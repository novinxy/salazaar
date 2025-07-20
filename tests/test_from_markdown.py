from collections.abc import Iterator
import glob
import itertools

import pytest


from tests.conftest import CodeTranspile, translate_and_compare


def parse_markdown_file(file_path: str) -> Iterator[CodeTranspile]:
    with open(file_path, mode='r', encoding='utf-8') as file:
        content = file.read()

    test_suite = content.split('# Test suite:', 1)[1].split('\n')[0].strip()

    test_cases = content.split('## Test case:')[1:]

    for test_case in test_cases:
        test_case_name = test_case.split('\n')[0].strip()

        yield CodeTranspile(
            id=f'{test_suite}-{test_case_name}',
            js=test_case.split('```js')[1].split('```')[0].strip(),
            py=test_case.split('```py')[1].split('```')[0].strip(),
        )

def get_tests():
    markdown_files = glob.glob("tests/*.md")

    return list(itertools.chain(*[
        parse_markdown_file(f) for f in markdown_files
    ]))


@pytest.mark.parametrize(
    "p",
    get_tests(),
    ids=CodeTranspile.get_pytest_id
    
)
def test_run_tests(p: CodeTranspile):
    translate_and_compare(p.js, p.py)

