"""Abstract Syntax Tree Nodes

This module defines classes for the AST nodes. A pretty print function is
included since I could not find a built-in one for Python that worked on trees
of objects (though the built-in pprint does a good job with dictionaries)
"""


class Program:
    def __init__(self, statements):
        self.statements = statements


class Declaration:
    def __init__(self, identifier, initializer):
        self.identifier = identifier
        self.initializer = initializer


class Assignment:
    def __init__(self, target, source):
        self.target = target
        self.source = source


class PrintStatement:
    def __init__(self, expression):
        self.expression = expression


class BinaryExpression:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryExpression:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class IdentifierExpression:
    def __init__(self, name):
        self.name = name


class LiteralExpression:
    def __init__(self, value):
        self.value = value


def print_tree(node, prefix='program', indent=0):
    print(f"{' ' * indent}{prefix}: {type(node).__name__}")
    indent += 2
    for attribute, child in node.__dict__.items():
        if isinstance(child, list):
            for index, node in enumerate(child):
                print_tree(node, f'{attribute}[{index}]', indent)
        elif '__dict__' in dir(child):
            print_tree(child, attribute, indent)
        else:
            print(f"{' ' * indent}{attribute}: {child}")
