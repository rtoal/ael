"""Compiler

This module exports a single function

    complile(source_code_string, output_type)

The second argument tells the compiler what to print to standard output. It
must be one of:

    tokens     the token sequence
    ast        the abstract syntax tree
    analyzed   the semantically analyzed representation
    optimized  the optimized semantically analyzed representation
    js         the translation to JavaScript
    c          the translation to C
    llvm       the translation to LLVM
"""

from ael.scanner import tokenize
from ael.parser import parse
from ael.analyzer import analyze
from ael.optimizer import optimize
from ael.generator import generate


def compile(source, output_type):
    output_type = output_type.lower()
    if output_type == 'tokens':
        for token in tokenize(source):
            print(token)
    elif output_type == 'ast':
        print(parse(source))
    elif output_type == 'analyzed':
        print(analyze(parse(source)))
    elif output_type == 'optimized':
        print(optimize(analyze(parse(source))))
    elif output_type in ('js', 'c', 'llvm'):
        print(generate[output_type](optimize(analyze(parse(source)))))
    else:
        print('Unknown output type')
