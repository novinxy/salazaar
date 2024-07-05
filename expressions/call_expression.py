
import ast


class CallExpression:
    def __init__(self, generic_parse) -> None:
        self.generic_parse = generic_parse

    def parse(self, expression):
        args = [self.generic_parse(arg) for arg in expression['arguments']]

        callee = expression['callee']

        func = self.generic_parse(callee)

        return ast.Call(
            func=func,
            args=args,
            keywords=[]
        )
