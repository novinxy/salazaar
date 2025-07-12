from dataclasses import dataclass
from textwrap import dedent

import pytest


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
