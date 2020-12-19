from scanner import tokenize


def test_scanner_can_tokenize_the_simplest_program():
    source = "   0   "
    tokens = list(tokenize(source))
    assert tokens == [('#NUMBER', '0'), ('#END', '')]
