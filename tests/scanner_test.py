from ael.scanner import tokenize


def test_scanner_can_tokenize_the_simplest_program():
    source = "   0   "
    tokens = list(tokenize(source))
    assert tokens == [('#NUMBER', '0'), ('#END', '')]


def test_scanner_can_tokenize_a_program_with_all_tokens():
    source = """   let x = 5 * 9
        x = x + (2 - 8) / 8999
        let y = x
        print y / 1
        """
    tokens = list(tokenize(source))
    assert tokens == [
        ('#KEYWORD', 'let'),
        ('#IDENTIFIER', 'x'),
        ('#SYMBOL', '='),
        ('#NUMBER', '5'),
        ('#SYMBOL', '*'),
        ('#NUMBER', '9'),
        ('#IDENTIFIER', 'x'),
        ('#SYMBOL', '='),
        ('#IDENTIFIER', 'x'),
        ('#SYMBOL', '+'),
        ('#SYMBOL', '('),
        ('#NUMBER', '2'),
        ('#SYMBOL', '-'),
        ('#NUMBER', '8'),
        ('#SYMBOL', ')'),
        ('#SYMBOL', '/'),
        ('#NUMBER', '8999'),
        ('#KEYWORD', 'let'),
        ('#IDENTIFIER', 'y'),
        ('#SYMBOL', '='),
        ('#IDENTIFIER', 'x'),
        ('#KEYWORD', 'print'),
        ('#IDENTIFIER', 'y'),
        ('#SYMBOL', '/'),
        ('#NUMBER', '1'),
        ('#END', '')]
