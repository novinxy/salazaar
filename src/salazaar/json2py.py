import argparse
from ast import Assign, Constant, Expr, FunctionDef, Load, Module, Store, arguments, Name
import ast
import json
import os

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
        '||': ast.Or()
    }

    values = []

    def parse_left(obj):
        if (obj['type'] == 'LogicalExpression'
            and obj['left']['type'] == 'LogicalExpression'
                and obj['operator'] == obj['left']['operator']):
            values1 = []
            values1 += parse_left(obj['left'])
            values1.append(parse_statement(obj['right']))
            return values1

        # if obj['type'] == 'LogicalExpression':
        #     values1 = []
        #     values1.append(parse_statement(obj['left']))
        #     values1.append(parse_statement(obj['right']))
        #     return values1

        return [parse_statement(obj)]

    values += parse_left(test_obj['left'])
    # values.append(parse_statement(test_obj['left']))
    values.append(parse_statement(test_obj['right']))

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
        'ForInStatement': parse_for_range,
        'ForOfStatement': parse_for_of,
    }[b.get('type')]

    return parser(b)


def parse_for_range(obj):

    iter = ast.Call(
        func=Name(id='range', ctx=Load()),
        args=[
            ast.Call(
                func=Name(id='len', ctx=Load()),
                args=[
                    parse_statement(obj['right'])
                ],
                keywords=[]
            )
        ],
        keywords=[]
    )

    body = parse_statement(obj['body'])

    return ast.For(
        iter=iter,
        target=Name(id=obj['left']['declarations'][0]['id']['name']),
        body=body,
        orelse=[]
    )

def parse_for_of(obj):
    iter = parse_statement(obj['right'])

    body = parse_statement(obj['body'])

    return ast.For(
        iter=iter,
        target=Name(id=obj['left']['declarations'][0]['id']['name']),
        body=body,
        orelse=[]
    )


def parse_array_expression(obj):
    elts = [parse_statement(e) for e in obj['elements']]
    return ast.List(elts=elts, ctx=Load())


def parse_member_expression(obj):

    _object = parse_statement(obj['object'])
    _property = parse_statement(obj['property'])

    if obj['computed']:
        return ast.Subscript(
            value=_object,
            slice=_property,
            ctx=Load()
        )

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
    return data.toDict()


def translate_code(js_code: str, export_ast: bool = False) -> str:
    js_ast = get_js_ast(js_code)

    if export_ast:
        os.makedirs('_out', exist_ok=True)
        with open('_out/js_tree.json', mode='w+', encoding='utf-8') as tf:
            json.dump(js_ast, tf, indent=4)

    py_ast = translate_ast(js_ast)

    if export_ast:
        with open('_out/py_tree.py', mode='w+', encoding='utf-8') as tf:
            tf.write(ast.dump(py_ast, indent=4))

    return ast.unparse(ast.fix_missing_locations(py_ast))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='temp.js', required=True)
    args = parser.parse_args()

    file_name = args.file
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    js_tree = get_js_ast(content)
    data = translate_ast(js_tree)
    # print(ast.dump(data, indent=4))

    data_str = ast.unparse(ast.fix_missing_locations(data))

    with open(file_name.replace('.js', '.py'), 'w+', encoding='utf-8') as f:
        f.write(data_str)


if __name__ == "__main__":
    main()
