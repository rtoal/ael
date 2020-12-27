import pytest
from ael.parser import parse
from ael.ast import *


def test_parser_can_parse_all_the_nodes():
    source = """
       let two = 2
       print(1 * two)   // TADA 🥑 
       two = sqrt 101.3"""
    assert str(parse(source)) == """   1 | program: Program
   2 |   statements[0]: Declaration name='two'
   3 |     initializer: LiteralExpression value=2
   4 |   statements[1]: PrintStatement
   5 |     expression: BinaryExpression op='*'
   6 |       left: LiteralExpression value=1
   7 |       right: IdentifierExpression name='two'
   8 |   statements[2]: Assignment
   9 |     target: IdentifierExpression name='two'
  10 |     source: UnaryExpression op='sqrt'
  11 |       operand: LiteralExpression value=101.3
"""


@ pytest.mark.parametrize("source", [
    "print 5 -",              # Missing right operand
    "print 7 * ((2 _ 3)",     # Missing right paren
    "print )",                # Illegal start of expression
    "x * 5",                  # Missing statement
    "print 5\nx * 5",         # Missing statement
    "let x = * 71"])
def test_parser_can_detect_lots_of_errors(source):
    with pytest.raises(Exception):
        print(parse(source))
