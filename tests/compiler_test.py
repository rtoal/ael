from ael.compiler import compile

sample_program = 'print 0'


def test_the_compile_function_understands_tokens():
    result = compile(sample_program, 'tokens')
    assert next(result) == ('#KEYWORD', 'print')


def test_the_compile_function_understands_ast():
    result = compile(sample_program, 'ast')
    assert str(result).startswith('   1 | program: Program')


def test_the_compile_function_understands_analyzed():
    result = compile(sample_program, 'analyzed')
    assert str(result).startswith('   1 | program: Program')


def test_the_compile_function_understands_optimized():
    result = compile(sample_program, 'optimized')
    assert str(result).startswith('   1 | program: Program')


def test_the_compile_function_understands_js():
    result = compile(sample_program, 'js')
    assert result.startswith('console.log(0)')


def test_the_compile_function_understands_c():
    result = compile(sample_program, 'c')
    assert result.startswith('#include')


def test_the_compile_function_understands_llvm():
    result = compile(sample_program, 'llvm')
    assert result.startswith('@format =')


def test_the_compile_function_prints_error_message_on_bad_output_type():
    result = compile(sample_program, 'llvmmmmm')
    assert result.startswith('Unknown output type')
