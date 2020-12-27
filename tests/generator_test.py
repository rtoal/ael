from textwrap import dedent
import pytest
from ael.scanner import tokenize
from ael.parser import parse
from ael.analyzer import analyze
from ael.optimizer import optimize
from ael.generator import generate

# Ideally there should be a ton of test cases here, right now we don't
# have many. Should have 100% coverage though.
javascript_fixtures = [(
    """\
    let x = 3
    x = 5 * sqrt x / x + x - abs x
    print x
    """,
    """\
    let x_1 = 3;
    x_1 = ((((5 * Math.sqrt(x_1)) / x_1) + x_1) - Math.abs(x_1));
    console.log(x_1);
    """
)]


@pytest.mark.parametrize("source, expected", [
    (dedent(ael), dedent(js)) for (ael, js) in javascript_fixtures])
def test_javascript_generator_works(source, expected):
    actual = generate['js'](optimize(analyze(parse(source))))
    assert actual == expected
