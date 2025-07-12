from dataclasses import dataclass
from textwrap import dedent
import textwrap

import pytest

from salazaar import salazaar


@pytest.fixture
def multiline():
    def clean(text: str) -> str:
        return dedent(text).strip("\n")

    return clean


@dataclass
class TestCaseParams:
    id: str
    __test__ = False

    def get_pytest_id(self):
        return self.id


@dataclass
class CodeTranspile(TestCaseParams):
    js: str
    py: str

    def __post_init__(self):
        self.js = textwrap.dedent(self.js).strip()
        self.py = textwrap.dedent(self.py).strip()


def translate_and_compare(js: str, py: str):
    result = salazaar.translate_code(js)

    assert result.strip() == py.strip(), f"Expected: {py}, but got: {result}"
