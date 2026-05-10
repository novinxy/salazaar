import re
from typing import Any

import itertools
import ast

from salazaar.ext_types import Empty, RawString, Comment


def is_typeof(node: dict):
    return node["type"] == "UnaryExpression" and node["operator"] == "typeof"


operators: dict[str, Any] = {
    "==": ast.Eq(),
    "!=": ast.NotEq(),
    "===": ast.Eq(),
    "!==": ast.NotEq(),
    ">": ast.Gt(),
    ">=": ast.GtE(),
    "<": ast.Lt(),
    "<=": ast.LtE(),
    "+": ast.Add(),
    "-": ast.Sub(),
    "*": ast.Mult(),
    "/": ast.Div(),
    "%": ast.Mod(),
    "**": ast.Pow(),
    "<<": ast.LShift(),
    ">>": ast.RShift(),
    "|": ast.BitOr(),
    "^": ast.BitXor(),
    "&": ast.BitAnd(),
    "++": ast.Add(),
    "--": ast.Sub(),
    "+=": ast.Add(),
    "-=": ast.Sub(),
    "*=": ast.Mult(),
    "/=": ast.Div(),
    "%=": ast.Mod(),
    "<<=": ast.LShift(),
    ">>=": ast.RShift(),
    "|=": ast.BitOr(),
    "^=": ast.BitXor(),
    "&=": ast.BitAnd(),
    "&&": ast.And(),
    "||": ast.Or(),
}


class JsConverter:
    def __init__(self):
        self.injected_blocks = []
        self.imports: set[str] = set()

    def add_import(self, import_: str):
        self.imports.add(import_)

    def prepend_to_parent(self, *block: ast.stmt):
        self.injected_blocks.extend(block)

    def prepend_from_child(self, body: list[ast.stmt]):
        if self.injected_blocks:
            body += self.injected_blocks
            self.injected_blocks = []

    def get_comments(self, node: dict) -> list[Comment]:
        comments = []
        for comment in node["leadingComments"]:
            if comment["type"] == "Block":
                comments += [Comment(value=c) for c in comment["value"].splitlines()]
            else:
                comments += [Comment(value=comment["value"])]
        return comments

    def visit(self, node: dict | None, default=None) -> Any:
        if node is None:
            return default

        method = f"visit_{node['type']}"
        visit_impl = getattr(self, method)

        if visit_impl is None:
            raise NotImplementedError(f'Method "{method}"" is not implemented')

        if "leadingComments" not in node:
            return visit_impl(node)

        comments = self.get_comments(node)

        res = visit_impl(node)
        if isinstance(res, list):
            return comments + res
        return comments + [res]

    def visit_EmptyStatement(self, _: dict):
        return Empty()

    def visit_Program(self, node: dict) -> ast.Module:
        nodes = [self.visit(n) for n in node["body"]]
        body = []

        for node in nodes:
            if node is None:
                continue

            if not isinstance(node, list):
                node = [node]

            self.prepend_from_child(body)
            body += node

        body = [ast.Import(names=[ast.alias(i)]) for i in self.imports] + body
        return ast.Module(body=body, type_ignores=[])

    def visit_UpdateExpression(self, node: dict):
        return ast.AugAssign(
            target=self.visit(node["argument"]),
            op=operators[node["operator"]],
            value=ast.Constant(value=1),
        )

    def visit_VariableDeclaration(self, node: dict):
        declarations = []
        for declaration in node["declarations"]:
            if declaration["id"]["type"] == "ArrayPattern":
                declarations.append(
                    ast.Assign(
                        targets=[ast.Tuple(elts=[ast.Name(i["name"]) for i in declaration["id"]["elements"]])],
                        value=ast.Tuple(elts=[self.visit(e) for e in declaration["init"]["elements"]]),
                    )
                )

                return declarations

            targets = [ast.Name(id=declaration["id"]["name"])]
            assigned_value = declaration.get("init", {"raw": "null", "type": "Literal", "value": "null"})

            match assigned_value["type"]:
                case "AssignmentExpression":
                    value = self.visit(assigned_value)
                    targets += value.targets
                    value = value.value
                case "FunctionExpression" if len(assigned_value["body"]["body"]) > 1:
                    return ast.FunctionDef(
                        name=declaration["id"]["name"],
                        args=ast.arguments(args=[ast.arg(p["name"]) for p in assigned_value["params"]]),
                        body=self.visit(assigned_value["body"]),
                    )
                case "ClassExpression":
                    bases = []
                    if base := assigned_value.get("superClass"):
                        bases = [self.visit(base)]

                    return ast.ClassDef(
                        name=declaration["id"]["name"],
                        bases=bases,
                        body=self.visit(assigned_value["body"]),
                    )
                case _:
                    value = self.visit(assigned_value)

            declarations.append(
                ast.Assign(
                    targets=targets,
                    value=value,
                )
            )

        return declarations

    def visit_Literal(self, node: dict) -> ast.Constant | RawString:
        if "regex" in node:
            self.add_import("re")

            return ast.Call(
                func=ast.Attribute(value=ast.Name(id="re"), attr="compile"),
                args=[RawString(value=node["regex"]["pattern"])],
                keywords=[],
            )

        value = node.get("value", "null")
        if value in ("undefined", "null"):
            return ast.Constant(value=None)

        if isinstance(value, re.Pattern):
            return RawString(value=value.pattern)
        return ast.Constant(value=value)

    def visit_Identifier(self, node: dict) -> ast.expr:
        name = node["name"]
        if name in ("undefined", "null"):
            return ast.Constant(value=None)

        mapping = {
            "Boolean": "bool",
            "Number": "float",
            "String": "str",
        }

        if name in mapping.keys():
            return ast.Name(id=mapping[name])

        return ast.Name(id=name)

    def visit_ExpressionStatement(self, node: dict):
        if node["expression"]["type"] in ("CallExpression", "MemberExpression", "BinaryExpression"):
            return ast.Expr(self.visit(node["expression"]))
        return self.visit(node["expression"])

    def visit_compare_typeof(self, node: dict):
        op = operators.get(node["operator"], None)

        # Both sides are typeof → type(a) == type(b)
        if is_typeof(node["left"]) and is_typeof(node["right"]):
            left_arg = self.visit(node["left"]["argument"])
            right_arg = self.visit(node["right"]["argument"])

            return ast.Compare(
                left=ast.Call(func=ast.Name(id="type"), args=[left_arg], keywords=[]),
                ops=[op],
                comparators=[ast.Call(func=ast.Name(id="type"), args=[right_arg], keywords=[])],
            )

        type_map = {
            "string": ast.Name(id="str"),
            "number": ast.Tuple(elts=[ast.Name(id="int"), ast.Name(id="float")]),
            "boolean": ast.Name(id="bool"),
            "object": ast.Name(id="object"),
        }

        if is_typeof(node["left"]):
            argument = self.visit(node["left"]["argument"])
            type_str = node["right"]["value"]
        else:
            argument = self.visit(node["right"]["argument"])
            type_str = node["left"]["value"]

        if type_str == "undefined":
            op = ast.Is() if isinstance(op, ast.Eq) else ast.IsNot()
            return ast.Compare(left=argument, ops=[op], comparators=[ast.Constant(value=None)])

        python_type = type_map.get(type_str, ast.Name(id="object"))
        isinstance_call = ast.Call(func=ast.Name(id="isinstance"), args=[argument, python_type], keywords=[])

        if not isinstance(op, ast.Eq):
            return ast.UnaryOp(op=ast.Not(), operand=isinstance_call)

        return isinstance_call

    def visit_BinaryExpression(self, node: dict):
        operator_ = node["operator"]

        left = self.visit(node["left"])
        right = self.visit(node["right"])

        if is_typeof(node["left"]) or is_typeof(node["right"]) and operator_ in ("==", "!=", "===", "!=="):
            return self.visit_compare_typeof(node)

        match operators.get(operator_, operator_):
            case ast.cmpop():
                return ast.Compare(left=left, ops=[operators[operator_]], comparators=[right])
            case ast.operator():
                return ast.BinOp(op=operators[operator_], left=left, right=right)
            case "in":
                return ast.Call(func=ast.Name("hasattr"), args=[right, left], keywords=[])
            case "instanceof":
                return ast.Call(func=ast.Name("isinstance"), args=[left, right], keywords=[])
            case _:
                raise ValueError(f"Incorrect operator: {operator_}")

    def visit_CallExpression(self, node: dict):
        args = [self.visit(arg) for arg in node["arguments"]]

        callee = node["callee"]

        if callee["type"] == "Super":
            return ast.Call(func=ast.Attribute(value=ast.Call(func=ast.Name(id="super")), attr="__init__"))

        if callee["type"] == "MemberExpression":
            if callee["property"]["name"] == "concat":

                def concat(argNum):
                    argNum -= 1
                    if argNum == 0:
                        return ast.BinOp(
                            left=self.visit(callee["object"]),
                            op=ast.Add(),
                            right=args[argNum],
                        )

                    return ast.BinOp(
                        left=concat(argNum),
                        op=ast.Add(),
                        right=args[argNum],
                    )

                return concat(len(args))

            if callee["property"]["name"] == "push":
                if len(args) <= 1:
                    return ast.Call(func=ast.Attribute(value=self.visit(callee["object"]), attr="append"), args=args)
                else:
                    return ast.Call(
                        func=ast.Attribute(value=self.visit(callee["object"]), attr="extend"),
                        args=[ast.List(elts=args)],
                    )
            if callee["property"]["name"] == "join":
                join_char = ast.Constant(value="")
                if args:
                    join_char = args[0]
                return ast.Call(func=ast.Attribute(value=join_char, attr="join"), args=[self.visit(callee["object"])])

            if callee["property"]["name"] == "slice":
                if len(args) == 1:
                    return ast.Subscript(
                        value=self.visit(callee["object"]),
                        slice=ast.Slice(lower=args[0]),
                    )
                if len(args) == 2:
                    return ast.Subscript(
                        value=self.visit(callee["object"]),
                        slice=ast.Slice(lower=args[0], upper=args[1]),
                    )
                return self.visit(callee["object"])

            if callee["property"]["name"] == "sort":
                if args:
                    self.add_import("functools")
                    return ast.Call(
                        func=ast.Attribute(value=self.visit(callee["object"]), attr="sort"),
                        keywords=[
                            ast.keyword(
                                arg="key",
                                value=ast.Call(
                                    func=ast.Attribute(value=ast.Name(id="functools"), attr="cmp_to_key"),
                                    args=args,
                                ),
                            )
                        ],
                    )

            if callee["property"]["name"] == "exec":
                self.add_import("re")
                return ast.Call(func=ast.Attribute(value=self.visit(callee["object"]), attr="search"), args=args)

            if callee["property"]["name"] == "test":
                self.add_import("re")
                return ast.Call(
                    func=ast.Name(id="bool"),
                    args=[ast.Call(func=ast.Attribute(value=self.visit(callee["object"]), attr="search"), args=args)],
                )

            if callee["property"]["name"] == "matchAll":
                self.add_import("re")
                return ast.Call(func=ast.Attribute(value=args[0], attr="finditer"), args=[self.visit(callee["object"])])

            if callee["property"]["name"] == "match":
                self.add_import("re")
                return ast.Call(func=ast.Attribute(value=args[0], attr="findall"), args=[self.visit(callee["object"])])

            if callee["object"].get("name") == "JSON":
                if callee["property"]["name"] == "parse":
                    self.add_import("json")
                    return ast.Call(func=ast.Attribute(value=ast.Name("json"), attr="loads"), args=args)

                if callee["property"]["name"] == "stringify":
                    self.add_import("json")
                    return ast.Call(func=ast.Attribute(value=ast.Name("json"), attr="dumps"), args=args)

            if callee["property"]["name"] == "trim":
                return ast.Call(func=ast.Attribute(value=self.visit(callee["object"]), attr="strip"), args=args)

            if callee["property"]["name"] == "split":
                if len(args) == 2:
                    return ast.Subscript(
                        value=ast.Call(
                            func=ast.Attribute(value=self.visit(callee["object"]), attr="split"), args=[args[0]]
                        ),
                        slice=ast.Slice(upper=args[1]),
                    )
                return ast.Call(func=ast.Attribute(value=self.visit(callee["object"]), attr="split"), args=args)
            if callee["property"]["name"] == "substr":
                if len(args) == 1:
                    return ast.Subscript(
                        value=self.visit(callee["object"]),
                        slice=ast.Slice(lower=args[0]),
                    )

                return ast.Subscript(
                    value=self.visit(callee["object"]),
                    slice=ast.Slice(lower=args[0], upper=ast.BinOp(left=args[0], op=ast.Add(), right=args[1])),
                )

            if callee["property"]["name"] == "substring":
                if len(args) == 1:
                    return ast.Subscript(
                        value=self.visit(callee["object"]),
                        slice=ast.Slice(lower=args[0]),
                    )

                return ast.Subscript(
                    value=self.visit(callee["object"]),
                    slice=ast.Slice(lower=args[0], upper=args[1]),
                )

            if callee["property"]["name"] == "toLowerCase":
                return ast.Call(func=ast.Attribute(value=self.visit(callee["object"]), attr="lower"), args=[])

            if callee["property"]["name"] == "toUpperCase":
                return ast.Call(func=ast.Attribute(value=self.visit(callee["object"]), attr="upper"), args=[])

            if callee["property"]["name"] == "toString":
                params = [self.visit(callee["object"])]
                return ast.Call(func=ast.Name(id="str"), args=params)

        func = self.visit(callee)

        return ast.Call(func=func, args=args, keywords=[])

    def visit_ObjectExpression(self, node: dict):
        keys = [self.visit(p["key"]) for p in node["properties"]]
        values = [self.visit(p["value"]) for p in node["properties"]]
        return ast.Dict(keys=keys, values=values)

    def visit_AssignmentExpression(self, node: dict):
        operator_ = operators.get(node["operator"], None)
        if operator_ is not None:
            return ast.AugAssign(
                target=self.visit(node["left"]),
                op=operator_,
                value=self.visit(node["right"]),
            )

        targets = [self.visit(node["left"])]
        rhs = node["right"]

        while rhs["type"] == "AssignmentExpression":
            targets.append(self.visit(rhs["left"]))

            rhs = rhs["right"]

        value = self.visit(rhs)

        if isinstance(value, list):
            raise ValueError("Value on the assign shouldn't be list", value)

        return ast.Assign(targets=targets, value=value)

    def visit_FunctionDeclaration(self, node: dict):
        name = node["id"]["name"]
        body = self.visit(node["body"])

        args, defaults = self.parse_function_params(node["params"])

        return ast.FunctionDef(
            name=name,
            args=ast.arguments(posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=defaults),
            body=body,
            decorator_list=[],
        )

    def parse_function_params(self, params: list[dict]) -> tuple[list[ast.arg], list[Any]]:
        args = []
        defaults = []
        for p in params:
            if p["type"] == "AssignmentPattern":
                args.append(ast.arg(arg=p["left"]["name"]))
                defaults.append(self.visit(p["right"]))
            else:
                args.append(ast.arg(arg=p["name"]))

        return args, defaults

    def visit_BlockStatement(self, node: dict):
        body = node["body"]

        if body == []:
            return [ast.Expr(ast.Constant(value=Ellipsis))]

        block = []

        for stmt in body:
            expression = self.visit(stmt)
            if not isinstance(expression, list):
                expression = [expression]

            self.prepend_from_child(block)

            block += expression

        return block

    def visit_LogicalExpression(self, node: dict):
        values = []

        def parse_left(obj: dict, op: str):
            if obj["type"] == "LogicalExpression" and op == obj["operator"]:
                values = []
                values += parse_left(obj["left"], obj["operator"])
                values.append(self.visit(obj["right"]))
                return values

            return [self.visit(obj)]

        operator_ = node["operator"]
        values += parse_left(node["left"], operator_)
        values.append(self.visit(node["right"]))

        return ast.BoolOp(op=operators[operator_], values=values)

    def visit_IfStatement(self, node: dict):
        orelse = self.visit(node.get("alternate"), [])
        if not isinstance(orelse, list):
            orelse = [orelse]

        body = self.visit(node["consequent"])
        if not isinstance(body, list):
            body = [body]

        return ast.If(
            test=self.visit(node["test"]),
            body=body,
            orelse=orelse,
        )

    def visit_ForInStatement(self, node: dict):
        iter_elem = ast.Call(
            func=ast.Name(id="range"),
            args=[ast.Call(func=ast.Name(id="len"), args=[self.visit(node["right"])], keywords=[])],
            keywords=[],
        )

        body = self.visit(node["body"])

        target = self.visit(node["left"])
        if node["left"]["type"] == "VariableDeclaration":
            target = ast.Name(id=node["left"]["declarations"][0]["id"]["name"])

        return ast.For(
            iter=iter_elem,
            target=target,
            body=body,
            orelse=[],
        )

    def visit_ForStatement(self, node: dict):
        init = [Empty()]
        test = ast.Constant(value=True)
        update = Empty()

        if "init" in node:
            init = self.visit(node.get("init"))
            if not isinstance(init, list):
                init = [init]
        if "test" in node:
            test = self.visit(node.get("test"))
        if "update" in node:
            update = self.visit(node.get("update"))

        if isinstance(update, ast.expr):
            update = ast.Expr(value=update)

        body = self.visit(node["body"])
        if not isinstance(body, list):
            body = [body]
        body.append(update)

        return [
            *init,
            ast.While(
                test=test,
                body=body,
                orelse=[],
            ),
        ]

    def visit_UnaryExpression(self, node: dict):
        op = {"-": ast.USub(), "~": ast.Invert(), "!": ast.Not(), "+": ast.UAdd()}.get(node["operator"])

        if op is not None:
            return ast.UnaryOp(op=op, operand=self.visit(node["argument"]))

        if node["operator"]:
            return ast.Call(func=ast.Name(id="type"), args=[self.visit(node["argument"])])

    def visit_ArrayExpression(self, node: dict):
        elements = [self.visit(e) for e in node["elements"]]
        return ast.List(elts=elements)

    def visit_MemberExpression(self, node: dict):
        value = self.visit(node["object"])

        if node["computed"]:
            return ast.Subscript(value=value, slice=self.visit(node["property"]))

        if node["property"]["name"] == "length":
            params = [self.visit(node["object"])]
            return ast.Call(func=ast.Name(id="len"), args=params)

        return ast.Attribute(value=value, attr=node["property"]["name"])

    def visit_ForOfStatement(self, node: dict):
        target = self.visit(node["left"])
        if node["left"]["type"] == "VariableDeclaration":
            target = ast.Name(id=node["left"]["declarations"][0]["id"]["name"])

        return ast.For(
            iter=self.visit(node["right"]),
            target=target,
            body=self.visit(node["body"]),
            orelse=[],
        )

    def visit_WhileStatement(self, node: dict):
        return ast.While(
            test=self.visit(node["test"]),
            body=self.visit(node["body"]),
            orelse=[],
        )

    def visit_DoWhileStatement(self, node: dict):
        body = self.visit(node["body"])

        return [
            body,
            ast.While(test=self.visit(node["test"]), body=body, orelse=[]),
        ]

    def visit_ReturnStatement(self, node: dict):
        return ast.Return(value=self.visit(node.get("argument")))

    def visit_BreakStatement(self, _: dict):
        return ast.Break()

    def visit_ContinueStatement(self, _: dict):
        return ast.Continue()

    def visit_ConditionalExpression(self, node: dict):
        return ast.IfExp(
            test=self.visit(node["test"]),
            body=self.visit(node["consequent"]),
            orelse=self.visit(node["alternate"]),
        )

    def visit_FunctionExpression(self, node: dict):
        node_body = node["body"]

        if len(node_body["body"]) > 1:
            func_name = "local_anonymous_func"
            if node.get("id"):
                func_name = node["id"]["name"]

            args, defaults = self.parse_function_params(node["params"])

            self.prepend_to_parent(
                ast.FunctionDef(
                    name=func_name,
                    args=ast.arguments(args=args, defaults=defaults),
                    body=self.visit(node_body),
                )
            )

            return ast.Name(id=func_name)

        if node_body["body"] == []:
            body = ast.Expr(ast.Constant(value=Ellipsis))
        else:
            body = self.visit(node_body["body"][0])

        if isinstance(body, ast.Expr) or isinstance(body, ast.Return):
            body = body.value

        return ast.Lambda(
            args=ast.arguments(args=[ast.arg(p["name"]) for p in node["params"]]),
            body=body,
        )

    def visit_ArrowFunctionExpression(self, node: dict):
        node_body = node["body"]

        if node_body["type"] == "BlockStatement" and len(node_body["body"]) > 1:
            args, defaults = self.parse_function_params(node["params"])

            self.prepend_to_parent(
                ast.FunctionDef(
                    name="local_anonymous_func",
                    args=ast.arguments(args=args, defaults=defaults),
                    body=self.visit(node_body),
                )
            )

            return ast.Name(id="local_anonymous_func")

        body = self.visit(node_body)
        if isinstance(body, list):
            body = body[0]

        if isinstance(body, ast.Expr) or isinstance(body, ast.Return):
            body = body.value

        return ast.Lambda(
            args=ast.arguments(args=[ast.arg(p["name"]) for p in node["params"]]),
            body=body,
        )

    def visit_SwitchStatement(self, node: dict):
        cases = []
        for idx, case_ in enumerate(node["cases"]):
            pattern = self.visit(case_.get("test"), ast.Name(id="_"))

            all_consequent = itertools.chain.from_iterable(c["consequent"] for c in node["cases"][idx::])
            all_cases = []
            for stmt in all_consequent:
                result = self.visit(stmt)
                if isinstance(result, list):
                    all_cases.extend(result)
                else:
                    all_cases.append(result)

            body = list(itertools.takewhile(lambda c: not isinstance(c, ast.Break), all_cases))

            if body == []:
                body += [ast.Expr(ast.Constant(value=Ellipsis))]

            cases.append(ast.match_case(pattern=pattern, body=body))

        return ast.Match(subject=self.visit(node["discriminant"]), cases=cases)

    def visit_TryStatement(self, node: dict):
        finalbody = []
        if "finalizer" in node:
            finalbody = self.visit(node["finalizer"])

        return ast.Try(
            body=self.visit(node["block"]),
            handlers=[self.visit(node.get("handler"), [])],
            finalbody=finalbody,
        )

    def visit_CatchClause(self, node: dict):
        return ast.ExceptHandler(
            type=ast.Name(id="Exception"),
            name=node["param"]["name"],
            body=self.visit(node["body"]),
        )

    def visit_ThrowStatement(self, node: dict):
        exc = self.visit(node["argument"])
        if node["argument"]["type"] == "Literal":
            exc = ast.Call(func=ast.Name("Exception"), args=[exc])

        return ast.Raise(exc=exc)

    def visit_ImportDeclaration(self, node: dict):
        module_name = node["source"]["value"].split(".")[0].replace("/", ".")

        if not node["specifiers"]:
            return ast.Import(names=[ast.alias(name=module_name)])

        if node["specifiers"][0]["type"] == "ImportNamespaceSpecifier":
            asname = node["specifiers"][0]["local"]["name"]
            if asname == module_name:
                asname = None
            return ast.Import(names=[ast.alias(name=module_name, asname=asname)])

        return ast.ImportFrom(
            module=module_name,
            names=[ast.alias(name=s["local"]["name"]) for s in node["specifiers"]],
            level=0,
        )

    def visit_ClassDeclaration(self, node: dict):
        bases = []
        if base := node.get("superClass"):
            bases = [self.visit(base)]

        return ast.ClassDef(
            name=node["id"]["name"],
            bases=bases,
            body=self.visit(node["body"]),
        )

    def visit_ClassBody(self, node: dict):
        class_body = [self.visit(n) for n in node["body"]]

        if class_body == []:
            class_body += [ast.Expr(ast.Constant(value=Ellipsis))]

        return class_body

    def visit_MethodDefinition(self, node: dict):
        body = self.visit(node["value"]["body"])

        params, defaults = self.parse_function_params(node["value"]["params"])
        decorators = [ast.Name(id="staticmethod")]

        if not node["static"]:
            decorators = []
            params = [ast.Name(id="self"), *params]

        func_name = "__init__"
        if node["kind"] != "constructor":
            func_name = node["key"]["name"]

        return ast.FunctionDef(
            name=func_name,
            args=ast.arguments(args=params, defaults=defaults),
            body=body,
            decorator_list=decorators,
        )

    def visit_ThisExpression(self, _: dict):
        return ast.Name(id="self")

    def visit_Super(self, _: dict):
        return ast.Call(func=ast.Name(id="super"))

    def visit_TemplateLiteral(self, node: dict):
        if not node["expressions"]:
            value = ast.Constant(value=node["quasis"][0]["value"]["raw"])
            return value

        joined_str = []
        for constant, expression in itertools.zip_longest(node["quasis"], node["expressions"]):
            if constant:
                joined_str.append(ast.Constant(constant["value"]["raw"]))
            if expression:
                joined_str.append(ast.FormattedValue(value=self.visit(expression), conversion=-1))

        return ast.JoinedStr(values=joined_str)

    def visit_NewExpression(self, node: dict):
        if node["callee"]["name"] == "RegExp":
            self.add_import("re")

            regexp_value = self.visit(node["arguments"][0])
            if node["arguments"][0]["type"] == "Literal":
                regexp_value = RawString(value=node["arguments"][0]["value"].replace("?<", "?P<"))

            return ast.Call(
                func=ast.Attribute(value=ast.Name(id="re"), attr="compile"), args=[regexp_value], keywords=[]
            )

        return ast.Call(
            func=self.visit(node["callee"]), args=[self.visit(arg) for arg in node["arguments"]], keywords=[]
        )

    def visit_SequenceExpression(self, node: dict):
        return [self.visit(e) for e in node["expressions"]]
