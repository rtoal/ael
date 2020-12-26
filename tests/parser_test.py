import pytest
from ael.parser import parse
from ael.ast import Program, Declaration, Assignment, PrintStatement
from ael.ast import IdentifierExpression, LiteralExpression
from ael.ast import BinaryExpression, UnaryExpression


def test_parser_can_parse_the_simplest_program():
    source = "   print   0  // TADA 🥑 "
    assert str(parse(source)) == str(
        Program([PrintStatement(LiteralExpression(0))]))


def test_parser_can_parse_another_simple_program():
    source = """
       let two = 2
       dog = sqrt 101.3"""
    assert str(parse(source)) == str(
        Program([
            Declaration('two', LiteralExpression(2)),
            Assignment(
                IdentifierExpression('dog'),
                UnaryExpression('sqrt', LiteralExpression(101.3)))]))


def test_parser_can_parse_program_with_everything():
    pass


@pytest.mark.parametrize("source", [
    "print 5 -",
    "print 7 * ((2 _ 3)",
    "print )",
    "let x = * 71"])
def test_parser_can_detect_lots_of_errors(source):
    with pytest.raises(Exception):
        print(parse(source))
