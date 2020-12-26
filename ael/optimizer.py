"""Optimizer

This module does machine independent optimizations on the analyzed semantic
graph.

The only optimizations supported here are:

    - assignments to self turn into no-ops
    - constant folding
    - some strength reductions (+0, -0, *0, *1, etc.)
"""

from ael.ast import *


def optimize(node):

    def optimizeProgram(self):
        self.statements = [optimize(s) for s in self.statements if s]
        return self

    def optimizeDeclaration(self):
        self.initializer = optimize(self.initializer)
        return self

    def optimizeAssignment(self):
        self.source = optimize(self.source)
        self.target = optimize(self.target)
        if isinstance(self.source, IdentifierExpression):
            if self.source.ref == self.target.ref:
                return None
        return self

    def optimizePrintStatement(self):
        self.expression = optimize(self.expression)
        return self

    def optimizeBinaryExpression(self):
        # Constant folding and a number of strength reductions!
        self.left = optimize(self.left)
        self.right = optimize(self.right)
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

    def optimizeUnaryExpression(self):
        import math
        self.operand = optimize(self.operand)
        if isinstance(self.operand, LiteralExpression):
            x = self.operand.value
            if self.op == '-':
                return LiteralExpression(-x)
            elif self.op == 'abs':
                return LiteralExpression(abs(x))
            elif self.op == 'sqrt':
                return LiteralExpression(math.sqrt(x))
        return self

    def optimizeIdentifierExpression(self):
        return self

    def optimizeLiteralExpression(self):
        return self

    return locals()[f"optimize{type(node).__name__}"](node)
