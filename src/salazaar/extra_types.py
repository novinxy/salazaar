import ast


class RawString(ast.AST):
    def __init__(self, value: str) -> None:
        self.value: str = value
        super().__init__()


class Comment(ast.AST):
    def __init__(self, value: str) -> None:
        self.value: str = value
        super().__init__()


class Empty(ast.AST):
    def __init__(self) -> None:
        super().__init__()
