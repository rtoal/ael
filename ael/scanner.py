"""Scanner

This is a hand-crafted scanner, using no external libraries at all. The
module exports a single generator function, tokenize, to which you pass the
source code of the program to tokenize.

Tokens are yielded as tuples of the form (category, lexeme). Categories
always begin with a # character. There are four types of categories, fully
listed in the following examples:

    ("#IDENTFIER", "x")
    ("#NUMBER", "153.8831")
    ("#SYMBOL", "+")
    ("#KEYWORD", "let")
"""

import re


def tokenize(source):
    SKIP = re.compile(r'\s+|//.*?(\n|$)')
    NUMBER = re.compile(r'\d+(\.\d+)?')
    KEYWORD = re.compile(r'(let|print|abs|sqrt)\b')
    IDENTIFIER = re.compile(r'\w+')
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
