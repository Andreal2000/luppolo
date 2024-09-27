from src.interpreter.expression import num, sym


def stdlib_expand(expr):
    """Expands a mathematical expression."""
    return expr.expand()


def stdlib_substitute(expr, match, subst):
    """Substitutes an expression `match` in the given expression `expr` with a new value `subst`."""
    return expr.substitute(match, subst)


def stdlib_eval(expr, *rat):
    """Evaluates the given expression with provided rational numbers."""
    return expr.eval(*rat)


def stdlib_simple_derive(expr, sym):
    """Computes the simple derivative of an expression with respect to a symbol."""
    return expr.simple_derive(sym)


def stdlib_derive_polynomial(poly, sym):
    """Derives a univariate polynomial with respect to a symbol."""
    return poly.derive_polynomial(sym)


def stdlib_input():
    """Reads input from the user and converts it to a number or symbol."""
    value = input()
    if value.isdigit():
        return num(int(value))
    elif len(value) == 1 and value.islower():
        return sym(value)
    else:
        raise Exception(f"Invalid input {value}")


def stdlib_print(expr):
    """Prints the given expression to the console."""
    print(expr)
    return expr


STDLIB = {
    "Expand": stdlib_expand,
    "Substitute": stdlib_substitute,
    "Eval": stdlib_eval,
    "SimpleDerive": stdlib_simple_derive,
    "DerivePolynomial": stdlib_derive_polynomial,
    "Input": stdlib_input,
    "Print": stdlib_print,
}
