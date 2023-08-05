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
                    Name(id=name,ctx=Store())
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
        "!=": ast.NotEq()
    }

    ops = [ops_map[test['operator']]]

    left = parse_statement(test['left'])

    rhs = test['right']['value']
    comparators = [Constant(value=rhs)]
    return ast.Compare(left=left,
                        ops=ops,
                        comparators=comparators)

        
def parse_if(bo):
    test = bo['test']
    return ast.If(
        test=parse_statement(test),
        body=parse_statement(
            bo['consequent']
        ),
        orelse=[]
    )

def parse_logical_expression(test_obj):
    operator_map = {
        '&&': ast.And(),
        '||': ast.Or(),
        '!': ast.Not()
    }
            
    values = []
    
    for v in [test_obj['left'], test_obj['right']]:
        values.append(parse_statement(v))
    
    return ast.BoolOp(
        op=operator_map[test_obj['operator']],
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


def parse_statement(b):
    if b['type'] == 'BlockStatement':
        return parse_body(b['body'])
    if b['type'] == 'VariableDeclaration':
        return parse_variable_declaration(b)
    if b['type'] == 'ExpressionStatement':
        return parse_expression(b)
    if b['type'] == 'CallExpression':
        return parse_call_expression(b)
    if b['type'] == 'IfStatement':
        return parse_if(b)
    if b['type'] == 'ReturnStatement':
        return parse_return(b)
    if b['type'] == 'FunctionDeclaration':
        return parse_function_declaration(b)
    if b['type'] == 'WhileStatement':
        return parse_while_loop(b)
    if b['type'] == 'BinaryExpression':
        return parse_binary_expr(b)
    if b['type'] == 'Literal':
        return parse_literal(b)
    if b['type'] == 'Identifier':
        return parse_identifier(b)
    if b['type'] == 'LogicalExpression':
        return parse_logical_expression(b)
    if b['type'] == 'MemberExpression':
        return parse_member_expression(b)
    if b['type'] == 'FunctionExpression':
        return parse_function_expression(b)


def parse_function_expression(b):
    


def parse_member_expression(obj):
    
    _object = parse_statement(obj['object'])
    _property = obj['property']['name']
    
    return ast.Attribute(
        value=_object,
        attr=_property,
        ctx=Load()
    )

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

def parse(js_code):
    js_tree = to_json(js_code)
    
    ast_ = Module(
        body=parse_body(js_tree['body']),
        type_ignores=[]
    )
    
    print(ast.dump(ast_, indent=4))
    return ast_
    
def to_json(js_code):

    # data = esprima.parse(content, options={'comment': True, 'range': True})
    data = esprima.parse(js_code)
    data = data.toDict()
    with open('result.json', 'w+') as f:
        json.dump(data, f, indent=4)
    return data
    

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='temp.js')
    args = parser.parse_args() 
    
    file_name = args.file
    with open(file_name, 'r') as f:
        content = f.read()
    data = parse(content)

    data_str = ast.unparse(ast.fix_missing_locations(data))

    with open(file_name.replace('.js', '.py'), 'w+') as f:
        f.write(data_str)

if __name__ == "__main__":
    main()

# tmp = {}
# if tmp['type'] == 'VariableDeclaration':
#     name = tmp['declarations'][0]['id']['name']
#     value = tmp['declarations'][0]['init']['raw']
#     z = f"""
#     Assign(
#         targets=[
#                 Name[id='{name}',ctx=Store())],
#         value=Constant(value={value}))
#     """