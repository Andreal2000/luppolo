from enum import Enum, auto


class TreeKind(Enum):
    BEGIN = auto()
    END = auto()
    JOIN = auto()

    PROGRAM = auto()
    FUNCTION = auto()
    BLOCK = auto()

    DECLARATION_INSTRUCTION = auto()
    FOREACH_INSTRUCTION = auto()
    IF_ELSE_INSTRUCTION = auto()
    IF_INSTRUCTION = auto()
    REPEAT_INSTRUCTION = auto()
    RETURN_INSTRUCTION = auto()
    WHILE_INSTRUCTION = auto()

    POW_EXPRESSION = auto()
    MUL_DIV_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    ADD_SUB_EXPRESSION = auto()

    FUNCTION_CALL_EXPRESSION = auto()

    NAT = auto()
    SYM = auto()
    ID = auto()
    BOOLEAN = auto()

    NOT_CONDITION = auto()
    AND_CONDITION = auto()
    OR_CONDITION = auto()
    COMPARISON_CONDITION = auto()


class Tree:
    def __init__(self, kind, children, value=None):
        self.kind = kind
        self.children = children
        self.value = value
        self.jumps = {}

    def __repr__(self) -> str:
        return self.kind.name + ("" if not self.value else f"({self.value})")

    def print(self, end=list()):
        pre = ""
        for i in end[:-1]:
            if i:
                pre += "   "
            else:
                pre += "│  "

        res = (
            pre
            + ("" if len(end) == 0 else "└──" if end[-1] else "├──")
            + str(self)
            + "\n"
        )

        if len(self.children) > 0:
            for child in self.children[:-1]:
                res += child.print(end + [False])
            if self.children[-1]:
                res += self.children[-1].print(end + [True])

        return res
