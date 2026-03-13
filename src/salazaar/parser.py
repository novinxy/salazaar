import ast
from _ast_unparse import Unparser

from salazaar.ext_types import RawString

class Parser(Unparser):
    def visit_RawString(self, node: RawString):

        super().write(f"r'{node.value}'")

    
    def unparse(self, node: ast.AST):
        return self.visit(ast.fix_missing_locations(node))
