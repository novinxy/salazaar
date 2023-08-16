import argparse
from ast import Assign, Constant, Expr, FunctionDef, Load, Module, Store, arguments, Name
import ast
import json

import esprima


def parse_variable_declaration(statement):
    declarations = []
    for d in statement['declarations']:
        name: str = d['id']['name']

        if statement.get('kind', '') == 'const':
            name = name.upper()

        declarations.append(
            Assign(
                targets=[
                    Name(id=name, ctx=Store())
                ],
                value=parse_statement(d['init'])
            )
        )

    return declarations


def parse_call_expression(expression):
    args = [parse_statement(arg) for arg in expression['arguments']]

    callee = expression['callee']

    func = parse_statement(callee)

    return ast.Call(
        func=func,
        args=args,
        keywords=[]
    )


def parse_expression(b):
    return Expr(
        value=parse_statement(b['expression'])
    )


def parse_return(b):
    return ast.Return(
        parse_statement(b['argument'])
    )


def parse_binary_expr(test):
    ops_map = {
        "==": ast.Eq(),
        "!=": ast.NotEq(),
        ">": ast.Gt(),
        ">=": ast.GtE(),
        "<": ast.Lt(),
        "<=": ast.LtE()
    }

    ops = [ops_map[test['operator']]]

    left = parse_statement(test['left'])
    right = parse_statement(test['right'])

    return ast.Compare(left=left,
                       ops=ops,
                       comparators=[right])


def parse_if(bo):
    orelse = []
    if alternate := bo.get('alternate'):
        orelse = parse_statement(alternate)
        if not isinstance(orelse, list):
            orelse = [orelse]

    return ast.If(
        test=parse_statement(bo['test']),
        body=parse_statement(bo['consequent']),
        orelse=orelse
    )


def parse_logical_expression(test_obj):
    bool_ops = {
        '&&': ast.And(),
        '||': ast.Or(),
        '!': ast.Not()
    }

    values = []

    for v in [test_obj['left'], test_obj['right']]:
        values.append(parse_statement(v))

    return ast.BoolOp(
        op=bool_ops[test_obj['operator']],
        values=values
    )


def parse_while_loop(b):
    test_value = parse_statement(b['test'])
    body = parse_statement(b['body'])

    return ast.While(
        test=test_value,
        body=body,
        orelse=[]
    )


def parse_literal(test_obj):
    return ast.Constant(value=test_obj['value'])


def parse_identifier(obj):
    return Name(id=obj['name'], ctx=Load())


def parse_unary_expression(obj):
    op = {
        '-': ast.USub(),
        '~': ast.Invert(),
        '!': ast.Not()
    }[obj['operator']]
    return ast.UnaryOp(
        op=op,
        operand=parse_statement(obj['argument'])
    )

def parse_object_expr(obj):
    keys = [parse_statement(p['key']) for p in obj['properties']]
    values = [parse_statement(p['value']) for p in obj['properties']]
    return ast.Dict(keys=keys,
                    values=values)

def parse_statement(b):
    if b is None:
        return []

    parser = {
        'BlockStatement': parse_block_statement,
        'VariableDeclaration': parse_variable_declaration,
        'ExpressionStatement': parse_expression,
        'CallExpression': parse_call_expression,
        'IfStatement': parse_if,
        'ReturnStatement': parse_return,
        'FunctionDeclaration': parse_function_declaration,
        'WhileStatement': parse_while_loop,
        'BinaryExpression': parse_binary_expr,
        'Literal': parse_literal,
        'Identifier': parse_identifier,
        'LogicalExpression': parse_logical_expression,
        'MemberExpression': parse_member_expression,
        'UnaryExpression': parse_unary_expression,
        'ArrayExpression': parse_array_expression,
        'ObjectExpression': parse_object_expr,
        #    'FunctionExpression': None,
        #    'ForInStatement': None,
        #    'ForOfStatement': None,
    }[b.get('type')]

    return parser(b)


def parse_array_expression(obj):
    elts = [parse_statement(e) for e in obj['elements']]
    return ast.List(elts=elts,
        ctx=Load())


def parse_member_expression(obj):

    _object = parse_statement(obj['object'])
    _property = obj['property']['name']

    return ast.Attribute(
        value=_object,
        attr=_property,
        ctx=Load()
    )


def parse_block_statement(obj):
    return parse_body(obj['body'])


def parse_body(body_statements):
    statements = []
    for b in body_statements:
        statement = parse_statement(b)
        if isinstance(statement, list):
            statements += statement
        else:
            statements.append(statement)
    return statements


def parse_function_declaration(statement):
    name = statement['id']['name']
    body = parse_statement(statement['body'])

    args = [ast.arg(arg=p['name']) for p in statement['params']]

    return FunctionDef(
        name=name,
        args=arguments(
            posonlyargs=[],
            args=args,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]),
        body=body,
        decorator_list=[]
    )


def translate_ast(js_ast: dict):
    body = parse_body(js_ast['body'])

    return Module(
        body=body,
        type_ignores=[]
    )


def get_js_ast(js_code: str) -> dict:
    data = esprima.parse(js_code)
    data = data.toDict()
    return data


def translate_code(js_code: str) -> str:
    js_tree = get_js_ast(js_code)
    with open('js_tree.json', mode='w+', encoding='utf-8') as tf:
        json.dump(js_tree, tf, indent=4)
    
    data = translate_ast(js_tree)
    with open('py_tree.py', mode='w+', encoding='utf-8') as tf:
        tf.write(ast.dump(data, indent=4))
    

    return ast.unparse(ast.fix_missing_locations(data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='temp.js')
    args = parser.parse_args()

    file_name = args.file
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    js_tree = get_js_ast(content)
    data = translate_ast(js_tree)
    # print(ast.dump(data, indent=4))

    data_str = ast.unparse(ast.fix_missing_locations(data))

    with open(file_name.replace('.js', '.py'), 'w+') as f:
        f.write(data_str)


if __name__ == "__main__":
    main()
