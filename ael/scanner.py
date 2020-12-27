"""Scanner

This is a hand-crafted scanner, using no external libraries at all. To scan,
create an instance of the Scanner class with the source code as a string, and
invoke, as-needed:

    match(t)
        Expect the next token to be t or in the set t, consume it, then return
        its lexeme. If the next token is not t or in the set t, raise an Error.

    match()
        Consume and return the next token, whatever it is.

    at(t)
        Whether or not the next token is t or in the set t.

Tokens are represented internally as tuples of the form (category, lexeme).
Categories always begin with a # character. Examples:

    ("#IDENTFIER", "x")
    ("#NUMBER", 32767)
    ("#SYMBOL", "+")
    ("#KEYWORD", "let")

When calling match() or at(), you can supply either a category or a lexeme:

    match("#IDENTIFIER")
    match("=")
    match({"+", "-", "#NUMBER"})
    at({"/", "*"})

This module also exports the tokenize function that the scanner uses to
generate the token sequence, good for inspecting the token stream.
"""

import re


def tokenize(source):
    SKIP = re.compile(r'\s+|//.*?(\n|$)')
    NUMBER = re.compile(r'\d+(\.\d+)?')
    KEYWORD = re.compile(r'(let|print|abs|sqrt)\b')
    IDENTIFIER = re.compile(r'\w+', re.UNICODE)
    SYMBOL = re.compile(r'\+|\-|\*|\/|=|\(|\)')

    position = 0
    while position < len(source):
        if match := SKIP.match(source, position):
            # Always begin by skipping whitespace and comments!
            position = match.end()
            continue
        if match := NUMBER.match(source, position):
            category = '#NUMBER'
        elif match := KEYWORD.match(source, position):
            # Must check keywords BEFORE identifiers!
            category = '#KEYWORD'
        elif match := IDENTIFIER.match(source, position):
            # Will only match if it was not a keyword matched earler
            category = '#IDENTIFIER'
        elif match := SYMBOL.match(source, position):
            category = '#SYMBOL'
        else:
            raise Exception(f"Unexpected character: '{source[position]}'")
        yield (category, match.group(0).strip())
        position = match.end()
    yield ('#END', '')


class Scanner:
    def __init__(self, source_code):
        self.stream = tokenize(source_code)
        self.advance()

    def advance(self):
        self.category, self.lexeme = next(self.stream)

    def at(self, candidate):
        if isinstance(candidate, set):
            return any(self.at(c) for c in candidate)
        if candidate.startswith('#'):
            return self.category == candidate
        return self.lexeme == candidate

    def match(self, expected_token=None, if_no_match=None):
        if expected_token is None or self.at(expected_token):
            matched_lexeme = self.lexeme
            self.advance()
            return matched_lexeme
        raise Exception(if_no_match or f"Expected '{expected_token}'")
