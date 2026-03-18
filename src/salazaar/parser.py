import ast

import sys

if sys.version_info < (3, 14):
    from ast import _Unparser as Unparser
else:
    from _ast_unparse import Unparser

from salazaar.ext_types import RawString, Comment


class Parser(Unparser):
    def visit_RawString(self, raw_string: RawString):
        self.write(f"r'{raw_string.value}'")

    def visit_Comment(self, comment: Comment):
        self.maybe_newline()
        self.write(f"# {comment.value.strip()}")

    def unparse(self, node: ast.AST):
        return self.visit(ast.fix_missing_locations(node))
