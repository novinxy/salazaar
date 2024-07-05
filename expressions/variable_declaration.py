import ast


class VariableDeclaration:
    def __init__(self, generic_parse) -> None:
        self.generic_parse = generic_parse

    def parse(self, statement: dict):
        declarations = []
        for declaration in statement['declarations']:
            name: str = declaration['id']['name']

            if statement.get('kind', '') == 'const':
                name = name.upper()

            declarations.append(
                ast.Assign(
                    targets=[
                        ast.Name(id=name, ctx=ast.Store())
                    ],
                    value=self.generic_parse(declaration['init'])
                )
            )

        return declarations