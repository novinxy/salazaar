from typing import Any
from ast import (
    ClassDef,
    alias,
    Add,
    And,
    Assign,
    Attribute,
    AugAssign,
    BinOp,
    BitAnd,
    BitOr,
    BitXor,
    BoolOp,
    Break,
    Call,
    Compare,
    Constant,
    Continue,
    Dict,
    Div,
    Eq,
    ExceptHandler,
    Expr,
    For,
    FunctionDef,
    Gt,
    GtE,
    If,
    IfExp,
    Import,
    ImportFrom,
    Invert,
    LShift,
    Lambda,
    List,
    Lt,
    LtE,
    Match,
    Mod,
    Module,
    Mult,
    Name,
    Not,
    NotEq,
    Or,
    Pow,
    RShift,
    Raise,
    Return,
    Sub,
    Subscript,
    Try,
    Tuple,
    USub,
    UnaryOp,
    While,
    arg,
    arguments,
    expr,
    match_case,
)


# pylint: disable=invalid-name

class ASTConverter:
    def __init__(self):
        self.injected_blocks = []

    def visit(self, node: dict|None) -> Any:
        if node is None:
            return None

        node_type = node["type"]
        method = "visit_" + node_type
        visitor = getattr(self, method)

        if visitor is None:
            raise NotImplementedError(f'Method "{method}"" is not implemented')

        return visitor(node)

    def visit_EmptyStatement(self, _: dict):
        return None

    def visit_Program(self, node: dict) -> Module:
        nodes = [self.visit(n) for n in node["body"]]
        body = []

        for n in nodes:
            if n is None:
                continue

            if not isinstance(n, list):
                n = [n]

            if self.injected_blocks:
                body += self.injected_blocks
                self.injected_blocks = []

            body += n

        return Module(body=body, type_ignores=[])

    def visit_UpdateExpression(self, node: dict):
        operator = node["operator"]
        match operator:
            case "++":
                return AugAssign(target=self.visit(node["argument"]), op=Add(), value=Constant(value=1))
            case "--":
                return AugAssign(target=self.visit(node["argument"]), op=Sub(), value=Constant(value=1))
            case _:
                raise ValueError(f"Incorrect operator {operator}")

    def visit_VariableDeclaration(self, node: dict):
        declarations = []
        for declaration in node["declarations"]:
            if declaration["id"]["type"] == "ArrayPattern":
                declarations.append(
                    Assign(
                        targets=[Tuple(elts=[Name(i["name"]) for i in declaration["id"]["elements"]])],
                        value=Tuple(elts=[self.visit(e) for e in declaration["init"]["elements"]]),
                    )
                )

                return declarations

            targets = [Name(id=declaration["id"]["name"])]
            assigned_value = declaration.get("init", {"raw": "null", "type": "Literal", "value": "null"})

            if assigned_value["type"] == "AssignmentExpression":
                value = self.visit(assigned_value)
                targets += value.targets
                value = value.value

            elif assigned_value["type"] == "FunctionExpression" and len(assigned_value["body"]["body"]) > 1:
                return FunctionDef(
                    name=declaration["id"]["name"],
                    args=arguments(args=[arg(p["name"]) for p in assigned_value["params"]]),
                    body=self.visit(assigned_value["body"]),
                )
            elif assigned_value['type'] == 'ClassExpression':
                bases = []
                if base := assigned_value.get('superClass'):
                    bases = [self.visit(base)]

                return ClassDef(
                    name=declaration['id']['name'],
                    bases=bases,
                    body=self.visit(assigned_value['body'])
                )
            else:
                value = self.visit(assigned_value)

            declarations.append(
                Assign(
                    targets=targets,
                    value=value,
                )
            )

        return declarations

    def visit_Literal(self, node: dict) -> Constant:
        value = node.get("value", "null")
        if value in ("undefined", "null"):
            return Constant(value=None)

        return Constant(value=value)

    def visit_Identifier(self, node: dict) -> expr:
        value = node["name"]
        if value in ("undefined", "null"):
            return Constant(value=None)

        return Name(id=value)

    def visit_ExpressionStatement(self, node: dict):
        if node["expression"]["type"] == "CallExpression":
            # TODO GRNO 2025-09-08 : This function creates issues with lambdas calls. Maybe there is other way around to write it in more elegant or direct way. Maybe we should only use Expr when we need it? But I guess that knowledge is only know if we know parent

            return Expr(self.visit(node["expression"]))
        return self.visit(node["expression"])

    def visit_BinaryExpression(self, node: dict):
        operators_mapping: dict[str, Any] = {
            "==": Eq(),
            "!=": NotEq(),
            "===": Eq(),
            "!==": NotEq(),
            ">": Gt(),
            ">=": GtE(),
            "<": Lt(),
            "<=": LtE(),
            "+": Add(),
            "-": Sub(),
            "*": Mult(),
            "/": Div(),
            "%": Mod(),
            "**": Pow(),
            "<<": LShift(),
            ">>": RShift(),
            "|": BitOr(),
            "^": BitXor(),
            "&": BitAnd(),
        }

        operator = node["operator"]
        left = self.visit(node["left"])
        right = self.visit(node["right"])

        match operator:
            case "==" | "!=" | "===" | "!==" | ">" | ">=" | "<" | "<=":
                return Compare(left=left, ops=[operators_mapping[operator]], comparators=[right])
            case "+" | "-" | "*" | "/" | "%" | "**" | "<<" | ">>" | "|" | "^" | "&":
                return BinOp(op=operators_mapping[operator], left=left, right=right)
            case "in":
                return Call(func=Name("hasattr"), args=[right, left], keywords=[])
            case "instanceof":
                return Call(func=Name("isinstance"), args=[left, right], keywords=[])
            case _:
                raise ValueError(f"Incorrect operator: {operator}")

    def visit_CallExpression(self, node: dict):
        args = [self.visit(arg) for arg in node["arguments"]]

        callee = node["callee"]

        if callee['type'] == 'Super':
            return Call(
                func=Attribute(
                    value=Call(func=Name(id='super')),
                    attr='__init__'
                )
            )

        func = self.visit(callee)

        return Call(func=func, args=args, keywords=[])

    def visit_ObjectExpression(self, node: dict):
        keys = [self.visit(p["key"]) for p in node["properties"]]
        values = [self.visit(p["value"]) for p in node["properties"]]
        return Dict(keys=keys, values=values)

    def visit_AssignmentExpression(self, node: dict):
        targets = []
        # TODO GRNO 2025-08-14 : are we sure about this line ?
        targets.append(self.visit(node["left"]))

        rhs = node["right"]

        operator = node["operator"]

        if operator == "=":
            # TODO GRNO 2025-08-19 : one again check it. I remember that it was for case with multiple assignments. But I need to double check it
            while rhs["type"] == "AssignmentExpression":
                targets.append(self.visit(rhs["left"]))

                rhs = rhs["right"]

            value = self.visit(rhs)

            if isinstance(value, list):
                raise ValueError("Value on the assign shouldn't be list", value)

            return Assign(targets=targets, value=value)

        operators = {
            "+=": Add(),
            "-=": Sub(),
            "*=": Mult(),
            "/=": Div(),
            "%=": Mod(),
            "<<=": LShift(),
            ">>=": RShift(),
            "|=": BitOr(),
            "^=": BitXor(),
            "&=": BitAnd(),
        }

        op = operators[operator]
        return AugAssign(target=self.visit(node["left"]), op=op, value=self.visit(node["right"]))

    def visit_FunctionDeclaration(self, node: dict):
        name = node["id"]["name"]
        body = self.visit(node["body"])

        args = [arg(arg=p["name"]) for p in node["params"]]

        return FunctionDef(
            name=name,
            args=arguments(posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=body,
            decorator_list=[],
        )

    def visit_BlockStatement(self, node: dict):
        body_statements = node["body"]

        block = []

        for b in body_statements:
            statement = self.visit(b)
            if not isinstance(statement, list):
                statement = [statement]

            if self.injected_blocks:
                block += self.injected_blocks
                self.injected_blocks = []

            block += statement

        return block

    def visit_LogicalExpression(self, node: dict):
        # TODO GRNO 2025-08-14 : hate this function. We should quickly fix this one

        bool_ops = {"&&": And(), "||": Or()}

        operator = node["operator"]

        values = []

        def parse_left(obj, operator):
            if (
                obj["type"] == "LogicalExpression"
                and operator == obj['operator']
            ):
                values1 = []
                values1 += parse_left(obj["left"], obj['operator'])
                values1.append(self.visit(obj["right"]))
                return values1

            return [self.visit(obj)]

        values += parse_left(node["left"], operator)
        # values.append(self.visit(node['left']))
        values.append(self.visit(node["right"]))

        return BoolOp(op=bool_ops[operator], values=values)

    def visit_IfStatement(self, node: dict):
        orelse = []
        if alternate := node.get("alternate"):
            orelse = self.visit(alternate)
            if not isinstance(orelse, list):
                orelse = [orelse]

        return If(test=self.visit(node["test"]), body=self.visit(node["consequent"]), orelse=orelse)

    def visit_ForInStatement(self, node: dict):
        iter_elem = Call(
            func=Name(id="range"),
            args=[Call(func=Name(id="len"), args=[self.visit(node["right"])], keywords=[])],
            keywords=[],
        )

        body = self.visit(node["body"])

        return For(iter=iter_elem, target=Name(id=node["left"]["declarations"][0]["id"]["name"]), body=body, orelse=[])

    def visit_ForStatement(self, node: dict):
        init = self.visit(node["init"])
        test = self.visit(node["test"])
        update = self.visit(node["update"])

        body = self.visit(node["body"])
        body.append(update)
        return [
            init[0],
            While(
                test=test,
                body=body,
                orelse=[],
            ),
        ]

    def visit_UnaryExpression(self, node: dict):
        operator = {"-": USub(), "~": Invert(), "!": Not()}[node["operator"]]

        return UnaryOp(op=operator, operand=self.visit(node["argument"]))

    def visit_ArrayExpression(self, node: dict):
        elements = [self.visit(e) for e in node["elements"]]
        return List(elts=elements)

    def visit_MemberExpression(self, node: dict):
        value = self.visit(node["object"])

        if node["computed"]:
            return Subscript(value=value, slice=self.visit(node["property"]))

        return Attribute(value=value, attr=node["property"]["name"])

    def visit_ForOfStatement(self, node: dict):
        iter_elem = self.visit(node["right"])

        body = self.visit(node["body"])

        return For(iter=iter_elem, target=Name(id=node["left"]["declarations"][0]["id"]["name"]), body=body, orelse=[])

    def visit_WhileStatement(self, node: dict):
        test_value = self.visit(node["test"])
        body = self.visit(node["body"])

        return While(test=test_value, body=body, orelse=[])

    def visit_DoWhileStatement(self, node: dict):
        test_value = self.visit(node["test"])
        body = self.visit(node["body"])

        return [body, While(test=test_value, body=body, orelse=[])]

    def visit_ReturnStatement(self, node: dict):
        return Return(value=self.visit(node.get("argument")))

    def visit_BreakStatement(self, node: dict):
        return Break()

    def visit_ContinueStatement(self, node: dict):
        return Continue()

    def visit_ConditionalExpression(self, node: dict):
        return IfExp(
            test=self.visit(node["test"]),
            body=self.visit(node["consequent"]),
            orelse=self.visit(node["alternate"]),
        )

    def visit_FunctionExpression(self, node: dict):
        node_body = node["body"]
        if len(node_body["body"]) != 1:
            func_name =  "local_anonymous_func"
            if node.get("id"):
                func_name = node["id"]["name"]

            self.injected_blocks.append(
                FunctionDef(
                    name=func_name,
                    args=arguments(args=[arg(p["name"]) for p in node["params"]]),
                    body=self.visit(node_body),
                )
            )

            return Name(id=func_name)
        body = node_body["body"][0]

        body = self.visit(body)

        if isinstance(body, Expr) or isinstance(body, Return):
            body = body.value

        return Lambda(args=arguments(args=[arg(p["name"]) for p in node["params"]]), body=body)

    def visit_ArrowFunctionExpression(self, node: dict):
        body = node["body"]

        if body['type'] == 'BlockStatement' and len(body['body']) != 1:
            self.injected_blocks.append(
                FunctionDef(
                    name="local_anonymous_func",
                    args=arguments(args=[arg(p["name"]) for p in node["params"]]),
                    body=self.visit(body),
                )
            )

            return Name(id='local_anonymous_func')

        body = self.visit(body)

        if isinstance(body, Expr) or isinstance(body, Return):
            body = body.value

        return Lambda(args=arguments(args=[arg(p["name"]) for p in node["params"]]), body=body)

    def visit_SwitchStatement(self, node: dict):
        cases = []
        for c in node["cases"]:
            case = self.visit_SwitchCase(c)

            cases.append(case)

        for c in cases:
            if c.body and isinstance(c.body[-1], Break):
                c.body.pop()

        return Match(subject=self.visit(node["discriminant"]), cases=cases)

    def visit_SwitchCase(self, node: dict):
        pattern = Name(id="_")
        if "test" in node:
            pattern = self.visit(node["test"])

        return match_case(pattern=pattern, body=[self.visit(c) for c in node["consequent"]])

    def visit_TryStatement(self, node: dict):
        # somehow bodies in here work strange as they are missing Expression for CallExpressions
        # it's not needed in other places and is safer that way
        # I'm thinking if maybe we should write special method for it and wrap calls

        result = Try(
            body=self.visit(node["block"]),
            handlers=[self.visit(node["handler"])],
        )

        if "finalizer" in node:
            result.finalbody = self.visit(node["finalizer"])

        return result

    def visit_CatchClause(self, node: dict):
        # somehow bodies in here work strange as they are missing Expression for CallExpressions
        # it's not needed in other places and is safer that way
        # I'm thinking if maybe we should write special method for it and wrap calls
        return ExceptHandler(
            type=Name(id="Exception"), name=node["param"]["name"], body=[self.visit(b) for b in node["body"]["body"]]
        )

    def visit_ThrowStatement(self, node: dict):
        exc = self.visit(node["argument"])
        if node["argument"]["type"] == "Literal":
            exc = Call(func=Name("Exception"), args=[exc])

        return Raise(exc=exc)

    def visit_ImportDeclaration(self, node: dict):
        module_name = node['source']['value'].split('.')[0].replace('/', '.')

        if node['specifiers']:
            if node['specifiers'][0]['type'] == 'ImportNamespaceSpecifier':
                asname = node['specifiers'][0]['local']['name']
                if asname == module_name:
                    asname = None
                return Import(
                    names=[alias(name=module_name, asname=asname)]
                )
            return ImportFrom(
                module=module_name,
                names=[alias(name=s['local']['name']) for s in node['specifiers']],
                level=0,
            )


        return Import(
            names=[alias(name=module_name)]
        )

    def visit_ClassDeclaration(self, node: dict):
        bases = []
        if base := node.get('superClass'):
            bases = [self.visit(base)]

        return ClassDef(
            name=node['id']['name'],
            bases=bases,
            body=self.visit(node['body'])
        )

    def visit_ClassBody(self, node: dict):
        return [
            self.visit(n) for n in node['body']
        ]

    def visit_MethodDefinition(self, node: dict):
        if node['kind'] == 'constructor':
            params = [Name(id='self'), *(self.visit(a) for a in node['value']['params'])]
            return FunctionDef(
                name='__init__',
                args=arguments(args=params),
                body=self.visit(node['value']['body'])
            )
        
    def visit_ThisExpression(self, node: dict):
        return Name(id='self')
    
    def visit_Super(self, node: dict):
        return Call(func=Name(id='super'))
        