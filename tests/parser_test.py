import pytest
from ael.parser import parse
from ael.ast import Program, Declaration, Assignment, PrintStatement
from ael.ast import IdentifierExpression, LiteralExpression
from ael.ast import BinaryExpression, UnaryExpression, text


def test_parser_can_parse_the_simplest_program():
    source = "   print 0   "
    assert text(parse(source)) == \
        text(Program([PrintStatement(LiteralExpression(0))]))
