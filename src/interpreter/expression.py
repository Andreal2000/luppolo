from collections import defaultdict
from fractions import Fraction
from itertools import product


def add(*a):
    """Creates an addition expression from the provided operands."""
    return Expression("A", *a)


def mul(*m):
    """Creates a multiplication expression from the provided operands."""
    return Expression("M", *m)


def pow(*p):
    """Creates an exponentiation expression from the provided base and exponent."""
    return Expression("P", *p)


def num(n):
    """Creates a number expression from the given value."""
    return Expression("N", n)


def sym(s):
    """Creates a symbol expression from the given symbol."""
    return Expression("S", s)


class Expression:
    def __init__(self, expr_type, *operands) -> None:
        """
        Initializes an `Expression` object based on the given type and operands.
        The expression is automatically simplified.
        """

        self.type = expr_type.upper()
        self.operands = []
        for op in operands:
            match op:
                case int() | float() | Fraction():
                    self.operands.append(Fraction(op) if self.type == "N" else num(op))
                case str():
                    self.operands.append(op if self.type == "S" else sym(op))
                case Expression():
                    self.operands.append(op)
                case _:
                    print(
                        "ERROR in Expression: Unknown type",
                        expr_type,
                        *operands,
                        type(op),
                    )

        match self.type:
            case "P":
                base = self.operands[0]
                exponent = self.operands[1]

                if base.type == "N" and exponent.type == "N":
                    return self.init_num(base[0] ** exponent[0])

                if base.type == "P" and base[1].type == "N" and exponent.type == "N":
                    return self.init_pow(base[0], num(base[1][0] * exponent[0]))

                match exponent:
                    case 0:
                        return self.init_num(1)
                    case 1:
                        return self.init_copy(base)

                match base:
                    case 0:
                        return self.init_num(0)
                    case 1:
                        return self.init_num(1)

                return self.init_pow(base, exponent)

            case "M":
                operands = self.operands.copy()
                numbers = num(1)
                powers = defaultdict(lambda: num(0))

                for operand in operands:
                    operand = operand

                    match operand.type:
                        case "N":
                            if operand == 0:
                                return self.init_num(0)
                            numbers = num(numbers[0] * operand[0])
                        case "A" | "S":
                            powers[operand] = add(powers[operand], 1)
                        case "P":
                            powers[operand[0]] = add(powers[operand[0]], operand[1])
                        case "M":
                            operands += operand.operands

                result = []
                for base, exponent in powers.items():
                    if exponent == 1:
                        result += [base]
                    elif exponent != 0:
                        result += [pow(base, exponent)]

                if result == []:
                    return self.init_copy(numbers)
                elif len(result) == 1 and numbers == 1:
                    return self.init_copy(result[0])

                result += [numbers] if numbers != 1 else []

                return self.init_mul(*sorted(result))

            case "A":
                operands = self.operands.copy()
                numbers = num(0)
                muls = defaultdict(lambda: 0)

                for operand in operands:
                    match operand.type:
                        case "N":
                            numbers = num(numbers[0] + operand[0])
                        case "M":
                            n = [i for i in operand.operands if i.type == "N"]

                            if n == []:
                                n = 1
                            else:
                                n = n[0][0]

                            not_n = [i for i in operand.operands if i.type != "N"]

                            if len(not_n) == 1:
                                not_n = not_n[0]
                            else:
                                not_n = mul(*not_n)

                            muls[not_n] += n
                        case "P" | "S":
                            muls[operand] += 1
                        case "A":
                            operands += operand.operands

                result = []
                for value, times in muls.items():
                    if times == 1:
                        result += [value]
                    elif times != 0:
                        result += [mul(times, value)]

                result += [numbers] if numbers != 0 else []

                if len(result) == 1:
                    return self.init_copy(result[0])
                elif len(result) == 0:
                    return self.init_num(0)

                return self.init_add(*sorted(result))

            case "N" | "S":
                pass

            case _:
                print("ERROR OPERANDS", self.type)

    def init_copy(self, expr):
        """Copies the type and operands from another expression into the current one."""
        self.type, self.operands = expr.type, expr.operands

    def init_add(self, *a):
        """Initializes the current expression as an addition expression."""
        self.type, self.operands = "A", list(a)

    def init_mul(self, *m):
        """Initializes the current expression as a multiplication expression."""
        self.type, self.operands = "M", list(m)

    def init_pow(self, *p):
        """Initializes the current expression as a power expression."""
        self.type, self.operands = "P", list(p)

    def init_num(self, n):
        """Initializes the current expression as a numeric expression."""
        self.type, self.operands = "N", [Fraction(n)]

    def init_sym(self, s):
        """Initializes the current expression as a symbolic expression."""
        self.type, self.operands = "S", [s]

    def __getitem__(self, key):
        """Accesses the operand at the specified index."""
        return self.operands[key]

    def __repr__(self) -> str:
        """Returns a string representation of the expression."""
        return self.print()

    def print_tree(self, verbous=False):
        """Prints the expression in a tree-like structure with the option for verbose output."""
        if self.type in ("N", "S"):
            return f"{self.type}({self[0]})" if verbous else str(self[0])
        else:
            return f"{self.type}({', '.join(map(lambda x: x.print_tree(verbous), self.operands))})"

    def print(self):
        """Returns the string representation of the expression similar to the one common used in math."""
        order = ["A", "M", "P", "N", "S"]
        index = order.index(self.type)

        match self.type:
            case "N" | "S":
                return str(self[0])

            case "A":
                operand_str = self.operands[0].print()
                result = (
                    operand_str
                    if order.index(self[0].type) > index
                    else f"({operand_str})"
                )
                for operand in self.operands[1:]:
                    operand_str = operand.print()

                    if operand.type == "N" and operand[0] < 0:
                        operand_str = f" - {abs(operand[0])}"
                    elif (
                        operand.type == "M"
                        and operand[0].type == "N"
                        and operand[0][0] < 0
                    ):
                        operand_str = f" - {operand_str[3:] if operand[0][0] == -1 else operand_str[1:]}"
                    elif (
                        operand.type == "P"
                        and operand[0].type == "N"
                        and operand[0][0] < 0
                    ):
                        operand_str = f" - {operand_str[1:]}"
                    else:
                        operand_str = f" + {operand_str}"

                    result += (
                        operand_str
                        if order.index(operand.type) > index
                        else f"{operand_str[:3]}({operand_str[3:]})"
                    )

                return result

            case "M":
                operand_str = self.operands[0].print()
                result = (
                    operand_str
                    if order.index(self[0].type) > index
                    else f"({operand_str})"
                )
                for operand in self.operands[1:]:
                    operand_str = operand.print()

                    if (
                        operand.type == "P"
                        and operand[1].type == "N"
                        and operand[1][0] <= -1
                    ):
                        den = pow(operand[0], abs(operand[1][0]))
                        operand_str = (
                            f"/{den if den.type in ['P', 'N', 'S'] else f'({den})'}"
                        )
                    else:
                        operand_str = f" * {operand_str}"

                    result += (
                        operand_str
                        if order.index(operand.type) > index
                        else f"{operand_str[:3]}({operand_str[3:]})"
                    )

                if result.startswith("-1 * -"):
                    result = result.replace("-1 * ", "+", 1)
                if result.startswith("-1 * "):
                    result = result.replace("-1 * ", "-", 1)

                return result

            case "P":
                base = self.operands[0]
                exp = self.operands[1]

                if exp.type == "N" and exp[0] <= -1:
                    den = pow(base, abs(exp[0]))
                    return f"1/{den if den.type in ['P', 'N', 'S'] else f'({den})'}"

                return "^".join(
                    map(
                        lambda x: x.print()
                        if order.index(x.type) > index
                        else f"({x.print()})",
                        self.operands,
                    )
                )

    def __hash__(self) -> int:
        """Returns the hash value for the expression."""
        return str(self).__hash__()

    def __eq__(self, value: object) -> bool:
        """Checks if the current expression is equal to the given value."""
        match value:
            case int() | float() | Fraction():
                return self.type == "N" and self[0] == value
            case str():
                return self.type == "S" and self[0] == value
            case Expression():
                return self.type == value.type and self.operands == value.operands

    def __lt__(self, value: object) -> bool:
        """Checks if the current expression is less than the given value."""
        order = ["N", "A", "S", "P", "M"]
        if type(value) is Expression:
            if order.index(self.type) == order.index(value.type):
                return self.operands < value.operands
            else:
                return order.index(self.type) < order.index(value.type)

    def __le__(self, value: object) -> bool:
        """Checks if the current expression is less than or equal to the given value."""
        return self < value or self == value

    def expand(self):
        """Expands the current expression by applying the algebraic properties of sums, products and powers."""

        def expand_pow(self):
            if self[1].type == "N":
                numerator, denominator = self[1][0].as_integer_ratio()

                if numerator < 0:
                    numerator *= -1
                    denominator *= -1

                base = expand_mul([self[0]] * numerator)

                if self[1][0].denominator == 1:
                    return base
                else:
                    return pow(base, 1 / denominator)
            else:
                return pow(*[e.expand() for e in self.operands])

        def expand_mul(operands):
            operands = operands.copy()
            result = operands[0].expand()
            for operand in operands[1:]:
                operand = operand.expand()
                if result.type == "A" and operand.type == "A":
                    result = add(
                        *[mul(*p) for p in product(result.operands, operand.operands)],
                    )
                elif result.type == "A" or operand.type == "A":
                    addition, other = (
                        (result, operand) if result.type == "A" else (operand, result),
                    )[0]
                    result = add(*[mul(a, other) for a in addition])
                else:
                    result = mul(result, operand)

            return result

        expand_table = {
            "P": expand_pow,
            "M": lambda node: expand_mul(node.operands),
            "A": lambda node: add(*[e.expand() for e in node.operands]),
            "S": lambda node: node,
            "N": lambda node: node,
        }
        return expand_table[self.type](self)

    def substitute(self, match, subst):
        """Substitutes occurrences of a specified expression `match` within the current expression with a new expression `subst`."""
        expr = Expression(self.type, *self.operands)

        for i in range(len(expr.operands)):
            if expr[i] == match:
                expr.operands[i] = subst
            elif type(expr[i]) is Expression and expr[i].type in ("A", "M", "P"):
                expr.operands[i] = expr[i].substitute(match, subst)

        return Expression(expr.type, *expr.operands)

    def find_symbols(self):
        """Finds all symbols within the expression."""
        if self.type == "S":
            return self[0]
        if self.type == "N":
            return set()

        symbols = set()
        for operand in self.operands:
            match operand.type:
                case "S":
                    symbols.add(operand)
                case "P" | "M" | "A":
                    symbols.update(operand.find_symbols())

        return symbols

    def eval(self, *rat):
        """
        Evaluates the expression by substituting the provided rational numbers for the symbols present in the expression.

        It substitutes each symbol with its corresponding rational number in alphabetical order.
        For example, calling `Eval(y^x, 2, 3)` substitutes `x` with `2` and `y` with `3`, resulting in `3^2`, which evaluates to `9`.
        """

        symbol = sorted(self.find_symbols())
        result = self

        if all(i.type != "N" for i in rat):
            raise Exception("Expected rational number")

        if len(symbol) == len(rat):
            for i in range(len(symbol)):
                result = result.substitute(symbol[i], rat[i])
            return result
        elif len(symbol) < len(rat):
            raise Exception(
                "Too much rational number to evaluate expression. "
                + f"Expected {len(symbol)}, but got {len(rat)}."
            )
        elif len(symbol) > len(rat):
            raise Exception(
                "Not enough rational number to evaluate expression. "
                + f"Expected {len(symbol)}, but got {len(rat)}."
            )

    def simple_derive(self, sym):
        """Calculates the derivative of the expression with respect to the given symbol."""

        def derive_pow(self):
            if self[1].type != "N":
                raise Exception("Non-rational exponent in expression")

            base = self[0]
            exp = self[1]

            return mul(
                exp,
                pow(base, add(exp, -1)),
                base.simple_derive(sym),
            )

        def derive_mul(self):
            result = []
            for i, item in enumerate(self.operands):
                other = self.operands[:i] + self.operands[i + 1 :]
                result += [mul(item.simple_derive(sym), *other)]

            return add(*result)

        if sym.type != "S":
            raise Exception("Second argument must be a symbol")

        derive_table = {
            "P": derive_pow,
            "M": derive_mul,
            "A": lambda node: add(*[n.simple_derive(sym) for n in node]),
            "S": lambda node: 0 if node != sym else 1,
            "N": lambda _: 0,
        }

        return derive_table[self.type](self)

    def derive_polynomial(self, sym):
        """Calculates the derivative of a univariate polynomial expression with respect to the given symbol."""
        if sym.type != "S":
            raise Exception("Second argument must be a symbol")

        expr = self.expand()
        symbols = sorted(expr.find_symbols())
        if len(symbols) == 1 and symbols[0] == sym:
            return expr.simple_derive(sym)
        else:
            raise Exception("Expression is not a univariate polynomial")
