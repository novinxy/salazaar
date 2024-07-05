from ast import *

Module(
    body=[
        If(
            test=Constant(value=False),
            body=[
                Assign(
                    targets=[
                        Name(id='tmp', ctx=Store())
],
                    value=Constant(value=10))
],
            orelse=[
                If(
                    test=Compare(
                        left=Name(id='i', ctx=Load()),
                        ops=[
                            Eq()
],
                        comparators=[
                            Constant(value=10)
]),
                    body=[
                        Assign(
                            targets=[
                                Name(id='tmp', ctx=Store())
],
                            value=Constant(value=20))
],
                    orelse=[
                        If(
                            test=Compare(
                                left=Name(id='i', ctx=Load()),
                                ops=[
                                    Eq()
],
                                comparators=[
                                    UnaryOp(
                                        op=USub(),
                                        operand=Constant(value=1))
]),
                            body=[
                                Assign(
                                    targets=[
                                        Name(id='tmp', ctx=Store())
],
                                    value=Constant(value=1))
],
                            orelse=[
                                If(
                                    test=Compare(
                                        left=Name(id='i', ctx=Load()),
                                        ops=[
                                            Eq()
],
                                        comparators=[
                                            Constant(value=50)
]),
                                    body=[
                                        Assign(
                                            targets=[
                                                Name(id='tmp', ctx=Store())
],
                                            value=Constant(value=100))
],
                                    orelse=[
                                        Assign(
                                            targets=[
                                                Name(id='tmp', ctx=Store())
],
                                            value=Constant(value=5000))
])
])
])
])
],
    type_ignores=[
])