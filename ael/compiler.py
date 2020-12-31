"""Compiler

This module exports a single function

    complile(source_code_string, output_type)

The second argument tells the compiler what to produce. It must be one of:

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
        return tokenize(source)
    elif output_type == 'ast':
        return(parse(tokenize(source)))
    elif output_type == 'analyzed':
        return(analyze(parse(tokenize(source))))
    elif output_type == 'optimized':
        return(optimize(analyze(parse(tokenize(source)))))
    elif output_type in ('js', 'c', 'llvm'):
        return(generate[output_type](optimize(analyze(parse(tokenize(source))))))
    else:
        return('Unknown output type')
