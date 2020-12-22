from ast import *


class Context:
    def __init__(self):
        # In real life, contexts are much larger than just a table: they would
        # also record the current function or module, whether you were in a
        # loop (for validating breaks and continues), and have a reference to
        # the parent contxt (to do static scope analysis) among other things.
        self.locals = {}

    def add_variable(self, name, variable):
        if name in self.locals:
            raise ValueError(f'Identifier {name} already declared')
        self.locals[name] = variable

    def lookup_variable(self, name):
        if variable := self.locals.get(name):
            return variable
        raise ValueError('Identifier {name} not declared')


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
    """This method is called by the compiler itself to begin the tree walk"""
    program.analyze(Context())
    return program


def show_graph(program):
    entities = {}

    def add_reachable_entities(node):
        if node and '__dict__' in dir(node) and node not in entities:
            entities[node] = len(entities)
            for key, value in node.__dict__.items():
                if isinstance(value, list):
                    for n in value:
                        add_reachable_entities(n)
                else:
                    add_reachable_entities(value)

    def ref(value):
        if isinstance(value, list):
            return f"[{','.join(ref(v) for v in value)}]"
        elif '__dict__' in dir(value):
            return f'#{entities.get(value)}'
        return repr(value)

    add_reachable_entities(program)
    for node, index in entities.items():
        attributes = [f'{k}={ref(v)}' for k, v in node.__dict__.items()]
        print(f'{index} ({type(node).__name__}) {" ".join(attributes)}')
