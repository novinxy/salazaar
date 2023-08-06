import ast


expr="""
if False:
    tmp = 10
elif i == 10:
    tmp = 20
"""
p=ast.dump(ast.parse(expr), indent=4)
print(p)