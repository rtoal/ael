"""A commpiler for Ael

You can run this compiler from the command line, for example:

    python ael.py -o some/cool/file.ael

or simply include this module in a larger app and invoke the compile function:

    compile(source_code_of_some_program, '-o')

The options are:
    * `-t`  Print the token stream then stop
    * `-a`  Print the AST then stop
    * `-i`  Print the analyzed AST (the semantic graph) then stop
    * `-o`  Print the optimzed, analyzed AST (the semantic graph) then stop

You can also invoke without an option string, in which case target code will be
generated.
"""

from scanner import tokenize
from parser import parse
from ast import print_tree
from analyzer import analyze, print_graph
from optimizer import optimize
from generator import generate


def compile(source, options):
    if options == '-t':
        for token in tokenize(source):
            print(token)
    elif options == '-a':
        print_tree(parse(source))
    elif options == '-i':
        print_graph(analyze(parse(source)))
    elif options == '-o':
        print_graph(optimize(analyze(parse(source))))
    elif options is None:
        print(generate(optimize(analyze(parse(source)))))
    else:
        print(f'Unrecognized option, only -t, -a, -i, -o are allowed')


if __name__ == '__main__':
    from sys import argv
    from pathlib import Path
    has_option = len(argv) > 1 and argv[1].startswith('-')
    has_filename = len(argv) > 2 if has_option else len(argv) > 1
    if not has_filename:
        print('Filename expected')
    else:
        filename = argv[2] if has_option else argv[1]
        options = argv[1] if has_option else None
        compile(Path(filename).read_text(), options=options)
