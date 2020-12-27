import pytest
from ael.analyzer import analyze
from ael.parser import parse


def test_analyzer_can_analyze_all_the_nodes():
    source = """
       let two = 2
       print(1 * two)
       two = sqrt 101.3"""
    assert str(analyze(parse(source))) == """   1 | program: Program
   2 |   statements[0]: Declaration name='two'
   3 |     initializer: LiteralExpression value=2
   4 |   statements[1]: PrintStatement
   5 |     expression: BinaryExpression op='*'
   6 |       left: LiteralExpression value=1
   7 |       right: IdentifierExpression name='two' ref=$2
   8 |   statements[2]: Assignment
   9 |     target: IdentifierExpression name='two' ref=$2
  10 |     source: UnaryExpression op='sqrt'
  11 |       operand: LiteralExpression value=101.3
"""


@pytest.mark.parametrize("source", [
    "print x",                # Undeclared identifier
    "let x = 1\nlet x = 1"])   # Redeclared identifier
def test_analyzer_can_detect_all_the_errors(source):
    with pytest.raises(Exception):
        print(analyze(parse(source)))
