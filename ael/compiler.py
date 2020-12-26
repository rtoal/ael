"""A commpiler for Ael

You can run this compiler from the command line, for example:

    ./aelc some/cool/file.ael output_type

or simply include this module in a larger app and invoke the compile function:

    compile(source_code_of_some_program, output_type)

to print the target program to standard output. The option tells the compiler
what to print to standard output:

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
        print('Unrecognized output type')


if __name__ == '__main__':
    import sys
    import pathlib
    if len(sys.argv) != 3:
        print('Syntax: aelc filename output_type')
    else:
        compile(pathlib.Path(sys.argv[1]).read_text(), sys.argv[2])
