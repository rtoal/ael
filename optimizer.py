"""Optimizer

This module does machine independent optimizations on the AST.
"""

from ast import Program, Declaration, Assignment, PrintStatement
from ast import IdentifierExpression, LiteralExpression
from ast import BinaryExpression, UnaryExpression


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
    # TODO check if these are the same
    self.source = self.source.optimize()
    self.target = self.target.optimize()
    return self


def optimize(program):
    return program
