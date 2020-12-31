"""Parser

This is a recursive descent parser. Each phrase rule ("non-termnial") gets
its own parsing function which returns a piece of the Abstract Syntax Tree or
raises an Exception. More information about Recursive Descent Parsing can be
found at https://en.wikipedia.org/wiki/Recursive_descent_parser.

The parser is implemented as a function accepting a token stream. It stores
the current token in the two local variables (category, lexeme). Rather than
using the variables directly it relies on two utility functions:

    match(t)
        Expect the next token to be t or in the set t, consume it, then return
        its lexeme. If the next token is not t or in the set t, raise an Error.

    match()
        Consume and return the next token, whatever it is.

    at(t)
        Whether or not the next token is t or in the set t.

When calling match() or at(), you can supply either a category or a lexeme:

    match("#IDENTIFIER")
    match("=")
    match({"+", "-", "#NUMBER"})
    at({"/", "*"})
"""

from ael.ast import *


def parse(token_stream):
    category, lexeme = next(token_stream)

    def at(candidate):
        if isinstance(candidate, set):
            return any(at(c) for c in candidate)
        if candidate.startswith('#'):
            return category == candidate
        return lexeme == candidate

    def match(expected_token=None):
        nonlocal category, lexeme
        if expected_token is None or at(expected_token):
            matched_lexeme = lexeme
            category, lexeme = next(token_stream)
            return matched_lexeme
        raise Exception(f"Expected '{expected_token}'")

    def parse_program():
        statements = []
        statements.append(parse_statement())
        while not at('#END'):
            statements.append(parse_statement())
        return Program(statements)

    def parse_statement():
        if at('let'):
            return parse_declaration()
        elif at('#IDENTIFIER'):
            return parse_assignment()
        elif at('print'):
            return parse_print_statement()
        else:
            raise Exception('Statement expected')

    def parse_declaration():
        match('let')
        target = match('#IDENTIFIER')
        match('=')
        source = parse_expression()
        return Declaration(target, source)

    def parse_assignment():
        target = match('#IDENTIFIER')
        match("=")
        source = parse_expression()
        return Assignment(IdentifierExpression(target), source)

    def parse_print_statement():
        match('print')
        return PrintStatement(parse_expression())

    def parse_expression():
        left = parse_term()
        while at({"+", "-"}):
            op = match()
            right = parse_term()
            left = BinaryExpression(op, left, right)
        return left

    def parse_term():
        left = parse_factor()
        while at({"*", "/"}):
            op = match()
            right = parse_factor()
            left = BinaryExpression(op, left, right)
        return left

    def parse_factor():
        if at('#NUMBER'):
            value = float(match())
            return LiteralExpression(
                int(value) if int(value) == value else value)
        elif at('#IDENTIFIER'):
            return IdentifierExpression(match())
        elif at({'-', 'abs', 'sqrt'}):
            op = match()
            return UnaryExpression(op, parse_factor())
        elif at('('):
            match()
            e = parse_expression()
            match(')')
            return e
        else:
            raise Exception("Expected id, number, unary operator, or '('")

    return parse_program()
