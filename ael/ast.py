"""Abstract Syntax Tree Nodes

This module defines classes for the AST nodes. Only the initializers are
defined here. Semantic analysis methods, optimization methods, and code
generation methods are added in other modules. This keeps the compiler
organized by phase.
"""

from io import StringIO


class Program:
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return text(self)


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


def text(node):
    # Return a compact but pretty string representation of the node graph,
    # taking care of cycles. Written here from scracth because the built-in
    # Python pprint library has a function that works fine on dictionaries
    # but not on custom classes (unless you were to write your own str
    # function for each class, which would be very tedious and not necessary
    # in this case).
    buffer = StringIO()
    seen = {}
    node_id = 0

    def subtree_text(node, prefix, indent):
        nonlocal node_id
        node_id += 1
        seen[node] = node_id
        descriptor = f"{' ' * indent}{prefix}: {type(node).__name__}"
        simple_attributes, complex_attributes = "", []
        for attribute, child in node.__dict__.items():
            if '__dict__' in dir(child) and child in seen:
                simple_attributes += f" {attribute}=${seen[child]}"
            elif isinstance(child, list) or '__dict__' in dir(child):
                complex_attributes.append((attribute, child))
            else:
                simple_attributes += f" {attribute}={repr(child)}"
        print(f"{node_id:4} | {descriptor}{simple_attributes}", file=buffer)
        for attribute, child in complex_attributes:
            if isinstance(child, list):
                for index, node in enumerate(child):
                    subtree_text(node, f'{attribute}[{index}]', indent + 2)
            else:
                subtree_text(child, attribute, indent + 2)

    subtree_text(node, prefix='program', indent=0)
    return buffer.getvalue()
