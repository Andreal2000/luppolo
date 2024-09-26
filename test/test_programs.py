import pytest

from src.interpreter.expression import add, mul, pow
from src.main import compile_source, run_ir


@pytest.mark.parametrize(
    "arg, expected_output",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (7, 5040),
        (8, 40320),
        (9, 362880),
        (10, 3628800),
    ],
)
def test_factorial(arg, expected_output):
    with open("test/test_src/programs/Factorial.lpp", "r") as file:
        src = file.read()

        ir = compile_source(src)
        output = run_ir(ir, args=[arg])

        assert output == expected_output

        file.close()


@pytest.mark.parametrize(
    "arg, expected_output",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (10, 55),
        (15, 610),
        (20, 6765),
    ],
)
def test_fibonacci(arg, expected_output):
    with open("test/test_src/programs/Fibonacci.lpp", "r") as file:
        src = file.read()

        ir = compile_source(src)
        output = run_ir(ir, args=[arg])

        assert output == expected_output

        file.close()


"1+x"
"2+x+x^2"
"6+x+x^4+2*x^2"
"42+x+x^8+3*x^2+5*x^4"
"1806+x+x^16+4*x^2+14*x^4+18*x^8"


@pytest.mark.parametrize(
    "arg, expected_output",
    [
        (0, add(1, "x")),
        (1, add(2, "x", pow("x", 2))),
        (2, add(6, "x", pow("x", 4), mul(2, pow("x", 2)))),
        (3, add(42, "x", pow("x", 8), mul(3, pow("x", 2)), mul(5, pow("x", 4)))),
        (
            4,
            add(
                1806,
                "x",
                pow("x", 16),
                mul(4, pow("x", 2)),
                mul(14, pow("x", 4)),
                mul(18, pow("x", 8)),
            ),
        ),
    ],
)
def test_squared_terms(arg, expected_output):
    with open("test/test_src/programs/SquareTerms.lpp", "r") as file:
        src = file.read()

        ir = compile_source(src)
        output = run_ir(ir, args=[arg])

        assert output == expected_output

        file.close()
