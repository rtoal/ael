"""Optimizer

This module does machine independent optimizations on the AST.

The only optimizations supported here are:

    - assignments to self turn into no-ops
    - constant folding
    - some strength reductions
"""

from ael.ast import Program, Declaration, Assignment, PrintStatement
from ael.ast import IdentifierExpression, LiteralExpression
from ael.ast import BinaryExpression, UnaryExpression


def new_method(cls):
    return lambda f: (setattr(cls, f.__name__, f) or f)


@new_method(Program)
def optimize(self):
    self.statements = [s.optimize() for s in self.statements if s]
    return self


@new_method(Declaration)
def optimize(self):
    self.initializer = self.initializer.optimize()
    return self


@new_method(Assignment)
def optimize(self):
    self.source = self.source.optimize()
    self.target = self.target.optimize()
    if isinstance(self.source, IdentifierExpression):
        if self.source.ref == self.target.ref:
            return None
    return self


@ new_method(PrintStatement)
def optimize(self):
    self.expression = self.expression.optimize()
    return self


@ new_method(BinaryExpression)
def optimize(self):
    # Constant folding and a number of strength reductions!
    self.left = self.left.optimize()
    self.right = self.right.optimize()
    if isinstance(self.left, LiteralExpression):
        x = self.left.value
        if isinstance(self.right, LiteralExpression):
            y = self.right.value
            if self.op == '+':
                return LiteralExpression(x + y)
            elif self.op == '-':
                return LiteralExpression(x - y)
            elif self.op == '*':
                return LiteralExpression(x * y)
            elif self.op == '/':
                return LiteralExpression(x / y)
        elif (x, self.op) in ((0, '+'), (1, '*')):
            return self.right
        elif (x, self.op) == (0, '-'):
            return LiteralExpression(-self.right.value)
        elif (x, self.op) in ((0, '*'), (0, '/')):
            return LiteralExpression(0)
    elif isinstance(self.right, LiteralExpression):
        y = self.right.value
        if (self.op, y) in (('+', 0), ('-', 0), ('*', 1), ('/', 1)):
            return self.left
        if (self.op, y) == ('*', 0):
            return LiteralExpression(0)
    return self


@ new_method(UnaryExpression)
def optimize(self):
    import math
    self.operand = self.operand.optimize()
    if isinstance(self.operand, LiteralExpression):
        x = self.operand.value
        if self.op == '-':
            return LiteralExpression(-x)
        elif self.op == 'abs':
            return LiteralExpression(abs(x))
        elif self.op == 'sqrt':
            return LiteralExpression(math.sqrt(x))
    return self


@ new_method(IdentifierExpression)
def optimize(self):
    return self


@ new_method(LiteralExpression)
def optimize(self):
    return self


def optimize(program):
    return program.optimize()
