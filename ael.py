from scanner import tokenize
from parser import parse
from ast import pretty_print
from semantics import analyze, optimize, show_graph
from generator import generate


def compile(source, options):
    if options == '-t':
        for token in tokenize(source):
            print(token)
    elif options == '-a':
        pretty_print(parse(source))
    elif options == 'i':
        show_graph(analyze(parse(source)))
    elif options == 'o':
        show_graph(optimize(analyze(parse(source))))
    elif options is None:
        print(generate(optimize(analyze(parse(source)))))
    else:
        print(f'Unrecognized option, only -t, -a, -i, -o are allowed')

# TODO GET COMMAND LINE ARGUMENTS AND READ FILE


sample = """
    let dozen = 4 * 3
    print (dozen / abs 34 - 0) + 7 * 100)
    """

compile(sample, '-a')
