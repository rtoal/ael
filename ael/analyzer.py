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


def analyze(program):
    # Called by the compiler itself to begin the tree walk

    def analyze(node, context):
        # Local function to analyze any node, switches on type"""

        def analyze_Program(self, context):
            for s in self.statements:
                analyze(s, context)

        def analyze_Declaration(self, context):
            analyze(self.initializer, context)
            context.add_variable(self.identifier, self)

        def analyze_Assignment(self, context):
            analyze(self.source, context)
            analyze(self.target, context)

        def analyze_PrintStatement(self, context):
            analyze(self.expression, context)

        def analyze_BinaryExpression(self, context):
            analyze(self.left, context)
            analyze(self.right, context)

        def analyze_UnaryExpression(self, context):
            analyze(self.operand, context)

        def analyze_IdentifierExpression(self, context):
            self.ref = context.lookup_variable(self.name)

        def analyze_LiteralExpression(self, context):
            pass

        locals()[f"analyze_{type(node).__name__}"](node, context)

    # Launch the analyzer on the root node with initial context
    analyze(program, Context())
    return program
