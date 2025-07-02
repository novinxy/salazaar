import pytest

from textwrap import dedent


@pytest.fixture
def multiline():
    def clean(text: str) -> str:
        return dedent(text).strip("\n")

    return clean
