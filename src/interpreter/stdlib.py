from src.interpreter.expression import num, sym


def stdlib_expand(expr):
    return expr.expand()


def stdlib_substitute(expr, match, subst):
    return expr.substitute(match, subst)


def stdlib_eval(expr, *rat):
    return expr.eval(*rat)


def stdlib_simple_derive(expr, sym):
    return expr.simple_derive(sym)


def stdlib_derive_polynomial(poly, sym):
    return poly.derive_polynomial(sym)


def stdlib_input():
    value = input()
    if value.isdigit():
        return num(int(value))
    elif len(value) == 1 and value.islower():
        return sym(value)
    else:
        raise Exception(f"Invalid input {value}")


def stdlib_print(expr):
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
