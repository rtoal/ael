"""Abstract Syntax Tree Nodes

This module defines classes for the AST nodes. Only the initializers are
defined here. Semantic analysis methods, optimization methods, and code
generation methods are added in other modules. This keeps the compiler
organized by phase.
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
    # Prints the AST in a nice compact fashion. Written here from scracth
    # because the built-in Python pprint library has a function that works
    # fine on dictionaries but not on custom classes (unless you were to
    # write your own str function for each class). For our purposes, this
    # simple tree walk actually does a fine job.
    simple_attributes, complex_attributes = "", []
    for attribute, child in node.__dict__.items():
        if isinstance(child, list) or '__dict__' in dir(child):
            complex_attributes.append((attribute, child))
        else:
            simple_attributes += f" {attribute}={repr(child)}"
    print(f"{' ' * indent}{prefix}: {type(node).__name__}{simple_attributes}")
    for attribute, child in complex_attributes:
        if isinstance(child, list):
            for index, node in enumerate(child):
                print_tree(node, f'{attribute}[{index}]', indent + 2)
        else:
            print_tree(child, attribute, indent + 2)
