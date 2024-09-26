import inspect
from operator import eq, ge, gt, le, lt

from src.interpreter.expression import Expression, add, mul, num, pow, sym
from src.interpreter.stdlib import STDLIB


def interpreter(program, fun_name="Main", args=[], trace=False):
    GLOBAL_MEMORY = {}
    STACK = []
    IP = 0

    function = program[fun_name]

    while True:
        instr = function[IP]

        if trace:
            print(fun_name, IP, instr, STACK, GLOBAL_MEMORY)

        IP = None

        match instr["kind"]:
            case "BEGIN" | "JOIN":
                pass
            case "END":
                raise Exception(f"ERROR in {fun_name}: Return not found")
            case "FUNCTION":
                params = instr["value"]["parameters"]
                if len(args) < len(params):
                    raise Exception(
                        f"Error in {fun_name}: Missing {len(params) - len(args)} args"
                    )
                elif len(args) > len(params):
                    raise Exception(f"Error in {fun_name}: Too much args")
                else:
                    GLOBAL_MEMORY = dict(zip(params, args))

            case "POW_EXPRESSION":
                right = STACK.pop()
                left = STACK.pop()
                STACK.append(pow(left, right))
            case "MUL_DIV_EXPRESSION":
                if instr["value"] == "*":
                    STACK.append(mul(STACK.pop(), STACK.pop()))
                elif instr["value"] == "/":
                    denominator = STACK.pop()
                    if denominator != 0:
                        STACK.append(mul(pow(denominator, -1), STACK.pop()))
                    else:
                        raise Exception(f"ERROR in {fun_name}: Division by zero")
            case "UNARY_EXPRESSION":
                if instr["value"] == "-":
                    STACK.append(mul(STACK.pop(), -1))
            case "ADD_SUB_EXPRESSION":
                if instr["value"] == "+":
                    STACK.append(add(STACK.pop(), STACK.pop()))
                elif instr["value"] == "-":
                    STACK.append(add(mul(STACK.pop(), -1), STACK.pop()))

            case "DECLARATION_INSTRUCTION":
                GLOBAL_MEMORY[instr["value"]] = STACK.pop()

            case "IF_INSTRUCTION" | "IF_ELSE_INSTRUCTION":
                IP = instr["jumps"]["true"] if STACK.pop() else instr["jumps"]["false"]

            case "RETURN_INSTRUCTION":
                return STACK.pop()

            case "FOREACH_INSTRUCTION":
                expr = STACK.pop()
                if type(expr) is Expression:
                    expr = expr.operands

                if len(expr) > 0:
                    GLOBAL_MEMORY[instr["value"]], *tail = expr
                    STACK.append(tail)
                    IP = instr["jumps"]["loop"]
                else:
                    IP = instr["jumps"]["next"]

            case "REPEAT_INSTRUCTION":
                count = STACK.pop()

                if count.type == "N":
                    count = count[0]
                else:
                    raise Exception(
                        f"ERROR in {fun_name}: Repeat expression is not natural"
                    )

                if count > 0:
                    STACK.append(add(count, -1))
                    IP = instr["jumps"]["loop"]
                else:
                    IP = instr["jumps"]["next"]

            case "WHILE_INSTRUCTION":
                if STACK.pop():
                    IP = instr["jumps"]["loop"]
                else:
                    IP = instr["jumps"]["next"]

            case "FUNCTION_CALL_EXPRESSION":
                name = instr["value"]["name"]

                if name in program:
                    len_params = len(program[name][1]["value"]["parameters"])
                    num_params = instr["value"]["parameters"]

                    if len_params != num_params:
                        raise Exception(
                            f"ERROR in {fun_name}: Called function {name} with incorrect number of parameters. "
                            + f"Expected {len_params}, but got {num_params}."
                        )

                    params = [STACK.pop() for _ in range(num_params)]
                    STACK.append(interpreter(program, name, params, trace))
                elif name in STDLIB:
                    func = STDLIB[name]

                    len_params = len(inspect.signature(func).parameters)
                    num_params = instr["value"]["parameters"]

                    if (name == "Eval" and num_params < 2) or (
                        name != "Eval" and len_params != num_params
                    ):
                        raise Exception(
                            f"ERROR in {fun_name}: Called function {name} with incorrect number of parameters. "
                            + f"Expected {len_params}, but got {num_params}."
                        )

                    params = reversed(
                        [STACK.pop() for _ in range(instr["value"]["parameters"])]
                    )
                    try:
                        STACK.append(func(*params))
                    except Exception as e:
                        raise Exception(f"ERROR in {name}: {e}")
                else:
                    raise Exception(
                        f"ERROR in {fun_name}: Called undefined function {name}"
                    )

            case "NAT":
                STACK.append(num(int(instr["value"])))
            case "SYM":
                STACK.append(sym(instr["value"]))
            case "ID":
                if instr["value"] in GLOBAL_MEMORY:
                    STACK.append(GLOBAL_MEMORY[instr["value"]])
                else:
                    raise Exception(
                        f"ERROR in {fun_name}: Undefined variable {instr['value']}"
                    )
            case "BOOLEAN":
                STACK.append(instr["value"] == "true")

            case "NOT_CONDITION":
                STACK.append(not STACK.pop())
            case "AND_CONDITION":
                STACK.append(STACK.pop() and STACK.pop())
            case "OR_CONDITION":
                STACK.append(STACK.pop() or STACK.pop())
            case "COMPARISON_CONDITION":
                right = STACK.pop()
                left = STACK.pop()
                op = {"<=": le, "<": lt, "==": eq, ">": gt, ">=": ge}
                STACK.append(op[instr["value"]](left, right))

            case _:
                raise Exception(
                    f"ERROR in {fun_name}: Unknown instruction {instr['kind']}"
                )

        if IP is None:
            IP = instr["jumps"]["next"]
