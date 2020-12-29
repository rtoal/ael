from ael.compiler import compile

sample_program = 'print 0'


def test_the_compile_function_understands_tokens(capsys):
    compile(sample_program, 'tokens')
    captured = capsys.readouterr()
    assert captured.out.startswith("('#KEYWORD', 'print')")


def test_the_compile_function_understands_ast(capsys):
    compile(sample_program, 'ast')
    captured = capsys.readouterr()
    assert captured.out.startswith('   1 | program: Program')


def test_the_compile_function_understands_analyzed(capsys):
    compile(sample_program, 'analyzed')
    captured = capsys.readouterr()
    assert captured.out.startswith('   1 | program: Program')


def test_the_compile_function_understands_optimized(capsys):
    compile(sample_program, 'optimized')
    captured = capsys.readouterr()
    assert captured.out.startswith('   1 | program: Program')


def test_the_compile_function_understands_js(capsys):
    compile(sample_program, 'js')
    captured = capsys.readouterr()
    assert captured.out.startswith('console.log(0)')


def test_the_compile_function_understands_c(capsys):
    compile(sample_program, 'c')
    captured = capsys.readouterr()
    assert captured.out.startswith('#include')


def test_the_compile_function_understands_llvm(capsys):
    compile(sample_program, 'llvm')
    captured = capsys.readouterr()
    assert captured.out.startswith('@format =')


def test_the_compile_function_prints_error_message_on_bad_output_type(capsys):
    compile(sample_program, 'llvmmmmm')
    captured = capsys.readouterr()
    assert captured.out.startswith('Unknown output type')
