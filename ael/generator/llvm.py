"""Code Generator Ael -> LLVM

Invoke generate(program) with the program node to get back the LLVM
translation as a string.
"""

from io import StringIO
from ast import *


def generate(program):
    buffer = StringIO()
    variable_mapping = {}
    next_suffix = -1

    def new_local():
        nonlocal next_suffix
        next_suffix += 1
        return f"%{next_suffix}"

    def generate(node):
        def emit(line):
            print(line, file=buffer)

        def generateProgram(self):
            emit('@format = private constant [3 x i8] c"%g\\0A"')
            emit("declare i64 @printf(i8*, ...)")
            emit("declare double @llvm.fabs(double)")
            emit("declare double @llvm.sqrt.f64(double)")
            emit("define i64 @main() {")
            emit("entry:")
            for s in self.statements:
                generate(s)
            emit("ret i64 0")
            emit("}")

        def generateDeclaration(self):
            source = generate(self.initializer)
            variable_mapping[self] = source
            if isinstance(source, float) or source.startswith('%'):
                return
            # LLVM is single-assignment and you cannot assign a constant
            # to a variable, so we only generate a variable if the source
            # is not a constant
            target = new_local()
            emit(f"{target} = {source}")

        def generateAssignment(self):
            source = generate(self.source)
            variable_mapping[self] = source
            if isinstance(source, float) or source.startswith('%'):
                return
            # Since LLVM is single assignment, assignments work exactly
            # like declarations! Easiest to create a new variable!
            target = new_local()
            emit(f"{target} = {source}")

        def generatePrintStatement(self):
            format = 'i8* getelementptr inbounds ([3 x i8], [3 x i8]* @format, i64 0, i64 0)'
            operand = f'double {generate(self.expression)}'
            emit(f'call i64 (i8*, ...) @printf({format}, {operand})')

        def generateBinaryExpression(self):
            op = {'+': 'fadd', '-': 'fsub', '*': 'fmul', '/': 'fdiv'}[self.op]
            x = generate(self.left)
            y = generate(self.right)
            z = new_local()
            emit(f'{z} = {op} double {x}, {y}')
            return z

        def generateUnaryExpression(self):
            x = generate(self.operand)
            if self.op == '-':
                source = f'fneg double {x}'
            elif self.op == 'abs':
                source = f'call double @llvm.fabs(double {x})'
            elif self.op == 'sqrt':
                source = f'call double @llvm.sqrt.f64(double {x})'
            y = new_local()
            emit(f'{y} = {source}')
            return y

        def generateIdentifierExpression(self):
            return variable_mapping[self.ref]

        def generateLiteralExpression(self):
            return float(self.value)

        return locals()[f"generate{type(node).__name__}"](node)

    generate(program)
    return buffer.getvalue()
