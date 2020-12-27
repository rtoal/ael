"""Parser

This is a recursive descent parser. Each category ("non-termnial") gets its
own parsing function which returns a piece of the Abstract Syntax Tree or
raises an Exception. More information about Recursive Descent Parsing can
be found at https://en.wikipedia.org/wiki/Recursive_descent_parser.

The parser is implemented as a single function which creates a scanner when it
begins.
"""

from ael.scanner import Scanner
from ael.ast import *


def parse(source_code):
    the_scanner = Scanner(source_code)
    at = the_scanner.at
    match = the_scanner.match

    def parse_program():
        statements = []
        statements.append(parse_statement())
        while at({'#IDENTIFIER', 'let', 'print'}):
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
            raise Exception('Expected id, number, operator, or "(')

    return parse_program()
