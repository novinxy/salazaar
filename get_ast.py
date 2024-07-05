import ast
from textwrap import dedent


expr=dedent(
"""
    False or True and True
"""
).strip('\n')
tree = ast.parse(expr)
p=ast.dump(tree, indent=4)
print(p)

print(ast.unparse(ast.fix_missing_locations(tree)))