from operator import add, eq, ge, gt, le, lt, sub

from src.ast.tree import Tree, TreeKind


def optimize(ast):
    match ast.kind:
        case (
            TreeKind.PROGRAM
            | TreeKind.FUNCTION
            | TreeKind.DECLARATION_INSTRUCTION
            | TreeKind.FOREACH_INSTRUCTION
            | TreeKind.RETURN_INSTRUCTION
            | TreeKind.FUNCTION_CALL_EXPRESSION
        ):
            for i in range(len(ast.children)):
                ast.children[i] = optimize(ast.children[i])

        case TreeKind.BLOCK:
            instructions = ast.children
            children = []
            for i in range(len(instructions)):
                instr = optimize(instructions[i])
                if type(instr) is list:
                    children.extend(instr)
                elif type(instr) is Tree:
                    children.append(instr)
                    if instr.kind is TreeKind.RETURN_INSTRUCTION:
                        break
            ast.children = children

        case TreeKind.POW_EXPRESSION:
            base = optimize(ast.children[0])
            exp = optimize(ast.children[1])

            if exp.kind is TreeKind.NAT and exp.value == "1":
                return base
            elif base.kind is TreeKind.NAT and exp.kind is TreeKind.NAT:
                return Tree(
                    TreeKind.NAT,
                    [],
                    str(int(base.value) ** int(exp.value)),
                )
            else:
                ast.children = [base, exp]

        case TreeKind.MUL_DIV_EXPRESSION:
            base = optimize(ast.children[0])
            exp = optimize(ast.children[1])

            if base.kind is TreeKind.NAT and base.value == "1":
                return exp
            elif exp.kind is TreeKind.NAT and exp.value == "1":
                return base
            elif base.kind is TreeKind.NAT and exp.kind is TreeKind.NAT:
                if ast.value == "*":
                    return Tree(
                        TreeKind.NAT,
                        [],
                        str(int(base.value) * int(exp.value)),
                    )
                elif ast.value == "/" and exp.value != "0":
                    res = int(base.value) / int(exp.value)
                    if res.is_integer():
                        return Tree(TreeKind.NAT, [], str(int(res)))
            else:
                ast.children = [base, exp]

        case TreeKind.UNARY_EXPRESSION:
            child = optimize(ast.children[0])
            if ast.value == "+":
                return child
            elif ast.value == "-":
                if child.kind is TreeKind.NAT:
                    return Tree(TreeKind.NAT, [], str(-int(child.value)))
                elif child.kind is TreeKind.UNARY_EXPRESSION and child.value == "-":
                    return child.children[0]
            else:
                ast.children[0] = child

        case TreeKind.ADD_SUB_EXPRESSION:
            op = {"+": add, "-": sub}
            base = optimize(ast.children[0])
            exp = optimize(ast.children[1])

            if base.kind is TreeKind.NAT and base.value == "0":
                return exp
            elif exp.kind is TreeKind.NAT and exp.value == "0":
                return base
            elif base.kind is TreeKind.NAT and exp.kind is TreeKind.NAT:
                return Tree(
                    TreeKind.NAT,
                    [],
                    str(op[ast.value](int(base.value), int(exp.value))),
                )
            else:
                ast.children = [base, exp]

        case TreeKind.IF_INSTRUCTION:
            condition = optimize(ast.children[0])
            block_true = optimize(ast.children[1])

            if condition.kind is TreeKind.BOOLEAN and condition.value == "true":
                return block_true.children
            else:
                ast.children[0] = condition
                ast.children[1] = block_true

        case TreeKind.IF_ELSE_INSTRUCTION:
            condition = optimize(ast.children[0])
            block_true = optimize(ast.children[1])
            block_flase = optimize(ast.children[2])

            if condition.kind is TreeKind.BOOLEAN:
                if condition.value == "true":
                    return block_true.children
                elif condition.value == "false":
                    return block_flase.children
            else:
                ast.children[0] = condition
                ast.children[1] = block_true
                ast.children[2] = block_flase

        case TreeKind.REPEAT_INSTRUCTION:
            times = optimize(ast.children[0])
            block = optimize(ast.children[1])

            if times.kind is TreeKind.NAT:
                value = int(times.value)
                if value == 1:
                    return block.children
                elif value < 1:
                    return None
            else:
                ast.children = [times, block]

        case TreeKind.WHILE_INSTRUCTION:
            condition = optimize(ast.children[0])
            block = optimize(ast.children[1])

            if condition.kind is TreeKind.BOOLEAN and condition.value == "false":
                return None
            else:
                ast.children = [condition, block]

        case TreeKind.NOT_CONDITION:
            child = optimize(ast.children[0])
            if child.kind is TreeKind.BOOLEAN:
                return Tree(TreeKind.BOOLEAN, [], str(child.value == "false").lower())
            elif child.kind is TreeKind.NOT_CONDITION:
                print("not not")
                return child.children[0]
            else:
                ast.children[0] = child

        case TreeKind.AND_CONDITION:
            base = optimize(ast.children[0])
            exp = optimize(ast.children[1])

            if base.kind is TreeKind.BOOLEAN and exp.kind is TreeKind.BOOLEAN:
                return Tree(
                    TreeKind.BOOLEAN,
                    [],
                    str(base.value == "true" and exp.value == "true").lower(),
                )
            else:
                ast.children = [base, exp]

        case TreeKind.OR_CONDITION:
            base = optimize(ast.children[0])
            exp = optimize(ast.children[1])

            if base.kind is TreeKind.BOOLEAN and exp.kind is TreeKind.BOOLEAN:
                return Tree(
                    TreeKind.BOOLEAN,
                    [],
                    str(base.value == "true" or exp.value == "true").lower(),
                )
            else:
                ast.children = [base, exp]

        case TreeKind.COMPARISON_CONDITION:
            op = {"<=": le, "<": lt, "==": eq, ">": gt, ">=": ge}
            base = optimize(ast.children[0])
            exp = optimize(ast.children[1])

            if base.kind is TreeKind.NAT and exp.kind is TreeKind.NAT:
                return Tree(
                    TreeKind.BOOLEAN,
                    [],
                    str(op[ast.value](int(base.value), int(exp.value))).lower(),
                )
            else:
                ast.children = [base, exp]

        case _:
            pass

    return ast
