import ast

from salazaar.ext_types import RawString

class Parser(ast._Unparser):
    def visit_RawString(self, node: RawString):

        super().write(f"r'{node.value}'")

    
    def unparse(self, node: ast.AST):
        return self.visit(ast.fix_missing_locations(node))
