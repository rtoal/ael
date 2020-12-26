"""Semantic Analyzer

Analyzes the AST by looking for semantic errors and resolving references. As
Ael is such a trivial language (with no static types, no loops, no functions,
no nested scopes), the only semantic errors detected are:

    - redeclaration of an identifier
    - use of an identifier that has not been declared

Checks are made relative to a semantic context that is passed to the analyzer
function for each node. Since there is only one "scope" in Ael, there's only
one context, but in more complex languages things get much more interesting.
"""

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

        def analyzeProgram(self, context):
            for s in self.statements:
                analyze(s, context)

        def analyzeDeclaration(self, context):
            analyze(self.initializer, context)
            context.add_variable(self.name, self)

        def analyzeAssignment(self, context):
            analyze(self.source, context)
            analyze(self.target, context)

        def analyzePrintStatement(self, context):
            analyze(self.expression, context)

        def analyzeBinaryExpression(self, context):
            analyze(self.left, context)
            analyze(self.right, context)

        def analyzeUnaryExpression(self, context):
            analyze(self.operand, context)

        def analyzeIdentifierExpression(self, context):
            # All identifiers must already be declared
            self.ref = context.lookup_variable(self.name)

        def analyzeLiteralExpression(self, context):
            pass

        locals()[f"analyze{type(node).__name__}"](node, context)

    # Launch the analyzer on the root node with initial context
    analyze(program, Context())
    return program
