from ael.ast import *


class Context:
    def __init__(self):
        # In real life, contexts are much larger than just a table: they would
        # also record the current function or module, whether you were in a
        # loop (for validating breaks and continues), and have a reference to
        # the parent contxt (to do static scope analysis) among other things.
        self.locals = {}

    def add_variable(self, name, variable):
        if name in self.locals:
            raise Exception(f'Identifier {name} already declared')
        self.locals[name] = variable

    def lookup_variable(self, name):
        if variable := self.locals.get(name):
            return variable
        raise Exception('Identifier {name} not declared')


def new_method(cls):
    return lambda f: (setattr(cls, f.__name__, f) or f)


@new_method(Program)
def analyze(self, context):
    for s in self.statements:
        s.analyze(context)


@new_method(Declaration)
def analyze(self, context):
    self.initializer.analyze(context)
    context.add_variable(self.identifier, self)


@new_method(Assignment)
def analyze(self, context):
    self.source.analyze(context)
    self.target.analyze(context)


@new_method(PrintStatement)
def analyze(self, context):
    self.expression.analyze(context)


@new_method(BinaryExpression)
def analyze(self, context):
    self.left.analyze(context)
    self.right.analyze(context)


@new_method(UnaryExpression)
def analyze(self, context):
    self.operand.analyze(context)


@new_method(IdentifierExpression)
def analyze(self, context):
    self.ref = context.lookup_variable(self.name)


@new_method(LiteralExpression)
def analyze(self, context):
    pass


def analyze(program):
    """Called by the compiler itself to begin the tree walk"""
    program.analyze(Context())
    return program
