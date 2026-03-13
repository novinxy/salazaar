import ast
from _ast_unparse import Unparser

from salazaar.ext_types import RawString, Comment

class Parser(Unparser):
    def visit_RawString(self, raw_string: RawString):

        super().write(f"r'{raw_string.value}'")

    def visit_Comment(self, comment: Comment):

        super().write(f"#{comment.value}")


        # visit_expr = getattr(super(), f"visit_{expr_type}")
        # visit_expr(comment.expr)


    def unparse(self, node: ast.AST):
        return self.visit(ast.fix_missing_locations(node))
