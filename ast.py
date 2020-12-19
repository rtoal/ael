class Program:
    def __init__(self, statements):
        self.statements = statements

    def analyze(self, context):
        for s in self.statements:
            s.analyze(context)


class Declaration:
    def __init__(self, identifier, initializer):
        self.identifier = identifier
        self.initializer = initializer

    def analyze(self, context):
        self.initializer.analyze(context)
        context.add_variable(self.identifier)


class Assignment:
    def __init__(self, target, source):
        self.target = target
        self.source = source

    def analyze(self, context):
        self.source.analyze(context)
        self.target.analyze(context)


class PrintStatement:
    def __init__(self, expression):
        self.expression = expression

    def analyze(self, context):
        self.expression.analyze()


class BinaryExpression:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def analyze(self, context):
        self.left.analayze(context)
        self.right.analayze(context)


class UnaryExpression:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def analyze(self, context):
        self.operand.analayze(context)


class IdentifierExpression:
    def __init__(self, name):
        self.name = name

    def analyze(self, context):
        self.ref = context.lookup_variable(self.name)


class LiteralExpression:
    def __init__(self, value):
        self.value = value

    def analyze(self, context):
        pass


def pretty_print(node, prefix='program', indent=0):
    print(f"{' ' * indent}{prefix}: {type(node).__name__}")
    indent += 2
    for key, value in node.__dict__.items():
        if isinstance(value, list):
            for index, node in enumerate(value):
                pretty_print(node, f'{key}[{index}]', indent)
        elif '__dict__' in dir(value):
            pretty_print(value, key, indent)
        else:
            print(f"{' ' * indent}{key}: {value}")
