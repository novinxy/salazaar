import ast


def parse_variable_declaration(statement):
    declarations = []
    for d in statement["declarations"]:
        if d["id"]["type"] == "ArrayPattern":
            declarations.append(
                ast.Assign(
                    targets=[ast.Tuple(elts=[ast.Name(i["name"]) for i in d["id"]["elements"]])],
                    value=ast.Tuple(elts=[parse_statement(e) for e in d["init"]["elements"]]),
                )
            )
            return declarations

        name: str = d["id"]["name"]

        value = parse_statement(d["init"])

        declarations.append(
            ast.Assign(
                # TODO: There can be multiple targets in a single declaration
                # For example: const a = 1, b = 2
                # or a, b = (1, 2)
                targets=[ast.Name(id=name)],
                value=value,
            )
        )

    return declarations


def parse_assignment(statement):
    targets = parse_statement(statement['left'])
    value = parse_statement(statement['right'])
    
    return ast.Assign(
        targets=[targets],
        value=value
    )



def parse_call_expression(expression):
    args = [parse_statement(arg) for arg in expression["arguments"]]

    callee = expression["callee"]

    func = parse_statement(callee)

    return ast.Call(func=func, args=args, keywords=[])


def parse_expression(b):
    return ast.Expr(value=parse_statement(b["expression"]))


def parse_return(b):
    return ast.Return(parse_statement(b["argument"]))


def parse_binary_expr(test):
    ops_map = {"==": ast.Eq(), "!=": ast.NotEq(), ">": ast.Gt(), ">=": ast.GtE(), "<": ast.Lt(), "<=": ast.LtE()}

    ops = [ops_map[test["operator"]]]

    left = parse_statement(test["left"])
    right = parse_statement(test["right"])

    return ast.Compare(left=left, ops=ops, comparators=[right])


def parse_if(bo):
    orelse = []
    if alternate := bo.get("alternate"):
        orelse = parse_statement(alternate)
        if not isinstance(orelse, list):
            orelse = [orelse]

    return ast.If(test=parse_statement(bo["test"]), body=parse_statement(bo["consequent"]), orelse=orelse)


def parse_logical_expression(test_obj):
    bool_ops = {"&&": ast.And(), "||": ast.Or()}

    values = []

    def parse_left(obj):
        if (
            obj["type"] == "LogicalExpression"
            and obj["left"]["type"] == "LogicalExpression"
            and obj["operator"] == obj["left"]["operator"]
        ):
            values1 = []
            values1 += parse_left(obj["left"])
            values1.append(parse_statement(obj["right"]))
            return values1

        # if obj['type'] == 'LogicalExpression':
        #     values1 = []
        #     values1.append(parse_statement(obj['left']))
        #     values1.append(parse_statement(obj['right']))
        #     return values1

        return [parse_statement(obj)]

    values += parse_left(test_obj["left"])
    # values.append(parse_statement(test_obj['left']))
    values.append(parse_statement(test_obj["right"]))

    return ast.BoolOp(op=bool_ops[test_obj["operator"]], values=values)


def parse_while_loop(b):
    test_value = parse_statement(b["test"])
    body = parse_statement(b["body"])

    return ast.While(test=test_value, body=body, orelse=[])


def parse_literal(test_obj):
    return ast.Constant(value=test_obj["value"])


def parse_identifier(obj):
    return ast.Name(id=obj["name"])


def parse_unary_expression(obj):
    op = {"-": ast.USub(), "~": ast.Invert(), "!": ast.Not()}[obj["operator"]]

    return ast.UnaryOp(op=op, operand=parse_statement(obj["argument"]))


def parse_object_expr(obj):
    keys = [parse_statement(p["key"]) for p in obj["properties"]]
    values = [parse_statement(p["value"]) for p in obj["properties"]]
    return ast.Dict(keys=keys, values=values)


def parse_statement(b):
    # TODO: This function returns list[expr] for expr. IT creates many annoying typing issues and bugs. FIX THIS
    if b is None:
        return []

    parser = {
        "BlockStatement": parse_block_statement,
        "VariableDeclaration": parse_variable_declaration,
        "ExpressionStatement": parse_expression,
        "CallExpression": parse_call_expression,
        "IfStatement": parse_if,
        "ReturnStatement": parse_return,
        "FunctionDeclaration": parse_function_declaration,
        "WhileStatement": parse_while_loop,
        "BinaryExpression": parse_binary_expr,
        "Literal": parse_literal,
        "Identifier": parse_identifier,
        "LogicalExpression": parse_logical_expression,
        "MemberExpression": parse_member_expression,
        "UnaryExpression": parse_unary_expression,
        "ArrayExpression": parse_array_expression,
        "ObjectExpression": parse_object_expr,
        #    'FunctionExpression': None,
        "ForInStatement": parse_for_range,
        "ForOfStatement": parse_for_of,
        "AssignmentExpression": parse_assignment,
    }[b.get("type")]

    return parser(b)


def parse_for_range(obj):
    iter_elem = ast.Call(
        func=ast.Name(id="range"),
        args=[ast.Call(func=ast.Name(id="len"), args=[parse_statement(obj["right"])], keywords=[])],
        keywords=[],
    )

    body = parse_statement(obj["body"])

    return ast.For(
        iter=iter_elem, target=ast.Name(id=obj["left"]["declarations"][0]["id"]["name"]), body=body, orelse=[]
    )


def parse_for_of(obj):
    iter_elem = parse_statement(obj["right"])

    body = parse_statement(obj["body"])

    return ast.For(
        iter=iter_elem, target=ast.Name(id=obj["left"]["declarations"][0]["id"]["name"]), body=body, orelse=[]
    )


def parse_array_expression(obj):
    elements = [parse_statement(e) for e in obj["elements"]]
    return ast.List(elts=elements)


def parse_member_expression(obj):
    value = parse_statement(obj["object"])

    if obj["computed"]:
        return ast.Subscript(value=value, slice=parse_statement(obj["property"]))

    return ast.Attribute(value=value, attr=obj["property"]["name"])


def parse_block_statement(obj):
    return parse_body(obj["body"])


def parse_body(body_statements):
    statements = []
    for b in body_statements:
        statement = parse_statement(b)
        if not isinstance(statement, list):
            statement = [statement]

        statements += statement

    return statements


def parse_function_declaration(statement):
    name = statement["id"]["name"]
    body = parse_statement(statement["body"])

    args = [ast.arg(arg=p["name"]) for p in statement["params"]]

    return ast.FunctionDef(
        name=name,
        args=ast.arguments(posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=[]),
        body=body,
        decorator_list=[],
    )


def parse_module(js_ast: dict):
    body = parse_body(js_ast["body"])

    return ast.Module(body=body, type_ignores=[])
