from src.ast.tree import Tree, TreeKind
from src.grammar.LuppoloParser import LuppoloParser
from src.grammar.LuppoloVisitor import LuppoloVisitor


class LuppoloAstVisitor(LuppoloVisitor):
    # Visit a parse tree produced by LuppoloParser#program.
    def visitProgram(self, ctx: LuppoloParser.ProgramContext):
        functions = [self.visit(child) for child in ctx.function()]
        return Tree(TreeKind.PROGRAM, functions)

    # Visit a parse tree produced by LuppoloParser#function.
    def visitFunction(self, ctx: LuppoloParser.FunctionContext):
        _, _, *id, _, _ = ctx.children
        return Tree(
            TreeKind.FUNCTION,
            [
                self.visit(ctx.block()),
            ],
            {
                "name": ctx.ID()[0].getText(),
                "parameters": [id[i].getText() for i in range(len(id)) if i % 2 == 0],
            },
        )

    # Visit a parse tree produced by LuppoloParser#block.
    def visitBlock(self, ctx: LuppoloParser.BlockContext):
        instructions = [self.visit(child) for child in ctx.instruction()]
        return Tree(TreeKind.BLOCK, instructions)

    # Visit a parse tree produced by LuppoloParser#declarationInstruction.
    def visitDeclarationInstruction(
        self, ctx: LuppoloParser.DeclarationInstructionContext
    ):
        return Tree(
            TreeKind.DECLARATION_INSTRUCTION,
            [
                self.visit(ctx.expression()),
            ],
            ctx.ID().getText(),
        )

    # Visit a parse tree produced by LuppoloParser#foreachInstruction.
    def visitForeachInstruction(self, ctx: LuppoloParser.ForeachInstructionContext):
        return Tree(
            TreeKind.FOREACH_INSTRUCTION,
            [
                Tree(TreeKind.ID, [], ctx.ID().getText()),
                self.visit(ctx.expression()),
                self.visit(ctx.block()),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#ifElseInstruction.
    def visitIfElseInstruction(self, ctx: LuppoloParser.IfElseInstructionContext):
        return Tree(
            TreeKind.IF_ELSE_INSTRUCTION,
            [
                self.visit(ctx.condition()),
                self.visit(ctx.block()[0]),
                self.visit(ctx.block()[1]),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#ifInstruction.
    def visitIfInstruction(self, ctx: LuppoloParser.IfInstructionContext):
        return Tree(
            TreeKind.IF_INSTRUCTION,
            [
                self.visit(ctx.condition()),
                self.visit(ctx.block()),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#repeatInstruction.
    def visitRepeatInstruction(self, ctx: LuppoloParser.RepeatInstructionContext):
        return Tree(
            TreeKind.REPEAT_INSTRUCTION,
            [
                self.visit(ctx.expression()),
                self.visit(ctx.block()),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#returnInstruction.
    def visitReturnInstruction(self, ctx: LuppoloParser.ReturnInstructionContext):
        return Tree(
            TreeKind.RETURN_INSTRUCTION,
            [
                self.visit(ctx.expression()),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#whileInstruction.
    def visitWhileInstruction(self, ctx: LuppoloParser.WhileInstructionContext):
        return Tree(
            TreeKind.WHILE_INSTRUCTION,
            [
                self.visit(ctx.condition()),
                self.visit(ctx.block()),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#nat.
    def visitNat(self, ctx: LuppoloParser.NatContext):
        return Tree(TreeKind.NAT, [], ctx.NAT().getText())

    # Visit a parse tree produced by LuppoloParser#callExpression.
    def visitCallExpression(self, ctx: LuppoloParser.CallExpressionContext):
        return self.visit(ctx.call())

    # Visit a parse tree produced by LuppoloParser#sym.
    def visitSym(self, ctx: LuppoloParser.SymContext):
        return Tree(TreeKind.SYM, [], ctx.SYM().getText())

    # Visit a parse tree produced by LuppoloParser#expressionParens.
    def visitExpressionParens(self, ctx: LuppoloParser.ExpressionParensContext):
        return self.visit(ctx.expression())

    # Visit a parse tree produced by LuppoloParser#pow.
    def visitPow(self, ctx: LuppoloParser.PowContext):
        return Tree(
            TreeKind.POW_EXPRESSION,
            [
                self.visit(ctx.expression()[0]),
                self.visit(ctx.expression()[1]),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#addSub.
    def visitAddSub(self, ctx: LuppoloParser.AddSubContext):
        return Tree(
            TreeKind.ADD_SUB_EXPRESSION,
            [
                self.visit(ctx.expression()[0]),
                self.visit(ctx.expression()[1]),
            ],
            ctx.op.text,
        )

    # Visit a parse tree produced by LuppoloParser#unary.
    def visitUnary(self, ctx: LuppoloParser.UnaryContext):
        return Tree(
            TreeKind.UNARY_EXPRESSION,
            [
                self.visit(ctx.expression()),
            ],
            ctx.op.text,
        )

    # Visit a parse tree produced by LuppoloParser#id.
    def visitId(self, ctx: LuppoloParser.IdContext):
        return Tree(TreeKind.ID, [], ctx.ID().getText())

    # Visit a parse tree produced by LuppoloParser#mulDiv.
    def visitMulDiv(self, ctx: LuppoloParser.MulDivContext):
        return Tree(
            TreeKind.MUL_DIV_EXPRESSION,
            [
                self.visit(ctx.expression()[0]),
                self.visit(ctx.expression()[1]),
            ],
            ctx.op.text,
        )

    # Visit a parse tree produced by LuppoloParser#not.
    def visitNot(self, ctx: LuppoloParser.NotContext):
        return Tree(
            TreeKind.NOT_CONDITION,
            [
                self.visit(ctx.condition()),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#comparison.
    def visitComparison(self, ctx: LuppoloParser.ComparisonContext):
        return Tree(
            TreeKind.COMPARISON_CONDITION,
            [
                self.visit(ctx.expression()[0]),
                self.visit(ctx.expression()[1]),
            ],
            ctx.op.text,
        )

    # Visit a parse tree produced by LuppoloParser#boolean.
    def visitBoolean(self, ctx: LuppoloParser.BooleanContext):
        return Tree(TreeKind.BOOLEAN, [], ctx.BOOLEAN().getText())

    # Visit a parse tree produced by LuppoloParser#or.
    def visitOr(self, ctx: LuppoloParser.OrContext):
        return Tree(
            TreeKind.OR_CONDITION,
            [
                self.visit(ctx.condition()[0]),
                self.visit(ctx.condition()[1]),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#and.
    def visitAnd(self, ctx: LuppoloParser.AndContext):
        return Tree(
            TreeKind.AND_CONDITION,
            [
                self.visit(ctx.condition()[0]),
                self.visit(ctx.condition()[1]),
            ],
        )

    # Visit a parse tree produced by LuppoloParser#conditionParens.
    def visitConditionParens(self, ctx: LuppoloParser.ConditionParensContext):
        return self.visit(ctx.condition())

    # Visit a parse tree produced by LuppoloParser#call.
    def visitCall(self, ctx: LuppoloParser.CallContext):
        _, _, *expressions, _ = ctx.children
        expressions = [expressions[i] for i in range(len(expressions)) if i % 2 == 0]
        return Tree(
            TreeKind.FUNCTION_CALL_EXPRESSION,
            list(map(self.visit, expressions)),
            {
                "name": ctx.ID().getText(),
                "parameters": len(expressions),
            },
        )
