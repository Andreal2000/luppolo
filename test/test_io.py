import pytest

from src.interpreter.expression import num, sym
from src.main import compile_source, run_ir


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        ("5", num(5)),
        ("x", sym("x")),
    ],
)
def test_input_function(monkeypatch, input_data, expected_output):
    src = "Main() { return Input() }"

    monkeypatch.setattr("builtins.input", lambda: input_data)

    ir = compile_source(src)
    output = run_ir(ir)

    assert output == expected_output


@pytest.mark.parametrize(
    "print_value",
    [
        5,
        "x",
        "1+x",
        "2+x+x^2",
        "6+x+x^4+2*x^2",
        "42+x+x^8+3*x^2+5*x^4",
        "1806+x+x^16+4*x^2+14*x^4+18*x^8",
    ],
)
def test_print_function(capsys, print_value):
    src = f"Main() {{ return Print({print_value}) }}"

    ir = compile_source(src)

    output = run_ir(ir)
    captured = capsys.readouterr().out.strip()

    assert str(output) == str(captured)
