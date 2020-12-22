"""Scanner

This is a hand-crafted scanner, using no helpers other than the built-in Python
regular expressions module re. To scan source code, create an instance of the
Scanner class with the source code, and on demand, invoke

    match(t)
        Expect the next token to be t or in the set t, consume it, then return
        it. If the next token is not t or in the set t, raise an Error.

    match()
        Consume and return the next token, whatever it is.

    at(t)
        Whether or not the next token is t or in the set t.

Each token is a tuple of the form (category, lexeme). Categories always begin
with a # character. When calling match or at, you can use either a category
or a lexeme.
"""

import re


def tokenize(source):
    SKIP = re.compile(r'\s+')
    NUMBER = re.compile(r'\d+')
    KEYWORD = re.compile(r'(let|print|abs|sqrt)\b')
    IDENTIFIER = re.compile(r'\w+', re.UNICODE)
    SYMBOL = re.compile(r'\+|\-|\*|\/|=|\(|\)')

    start = 0
    while start < len(source):
        if match := SKIP.match(source, start):
            # Always begin by skipping whitespace and comments!
            start = match.end()
            continue
        if match := NUMBER.match(source, start):
            category = '#NUMBER'
        elif match := KEYWORD.match(source, start):
            # Keywords are checked BEFORE identifiers so that
            # no identifier can be a keyword
            category = '#KEYWORD'
        elif match := IDENTIFIER.match(source, start):
            category = '#IDENTIFIER'
        elif match := SYMBOL.match(source, start):
            category = '#SYMBOL'
        else:
            raise ValueError(f'Unexpected character: {source[start]}')
        yield (category, match.group(0).strip())
        start = match.end()
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

    def match(self, expected_token=None):
        if expected_token is None or self.at(expected_token):
            matched_lexeme = self.lexeme
            self.advance()
            return matched_lexeme
        raise SyntaxError(f'Expected {expected_token}')
