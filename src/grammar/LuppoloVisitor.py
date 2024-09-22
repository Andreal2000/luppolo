# Generated from Luppolo.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .LuppoloParser import LuppoloParser
else:
    from LuppoloParser import LuppoloParser

# This class defines a complete generic visitor for a parse tree produced by LuppoloParser.

class LuppoloVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LuppoloParser#program.
    def visitProgram(self, ctx:LuppoloParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#function.
    def visitFunction(self, ctx:LuppoloParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#block.
    def visitBlock(self, ctx:LuppoloParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#declarationInstruction.
    def visitDeclarationInstruction(self, ctx:LuppoloParser.DeclarationInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#foreachInstruction.
    def visitForeachInstruction(self, ctx:LuppoloParser.ForeachInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#ifElseInstruction.
    def visitIfElseInstruction(self, ctx:LuppoloParser.IfElseInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#ifInstruction.
    def visitIfInstruction(self, ctx:LuppoloParser.IfInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#repeatInstruction.
    def visitRepeatInstruction(self, ctx:LuppoloParser.RepeatInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#returnInstruction.
    def visitReturnInstruction(self, ctx:LuppoloParser.ReturnInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#whileInstruction.
    def visitWhileInstruction(self, ctx:LuppoloParser.WhileInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#nat.
    def visitNat(self, ctx:LuppoloParser.NatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#callExpression.
    def visitCallExpression(self, ctx:LuppoloParser.CallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#sym.
    def visitSym(self, ctx:LuppoloParser.SymContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#expressionParens.
    def visitExpressionParens(self, ctx:LuppoloParser.ExpressionParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#pow.
    def visitPow(self, ctx:LuppoloParser.PowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#addSub.
    def visitAddSub(self, ctx:LuppoloParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#unary.
    def visitUnary(self, ctx:LuppoloParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#id.
    def visitId(self, ctx:LuppoloParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#mulDiv.
    def visitMulDiv(self, ctx:LuppoloParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#not.
    def visitNot(self, ctx:LuppoloParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#comparison.
    def visitComparison(self, ctx:LuppoloParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#boolean.
    def visitBoolean(self, ctx:LuppoloParser.BooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#or.
    def visitOr(self, ctx:LuppoloParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#and.
    def visitAnd(self, ctx:LuppoloParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#conditionParens.
    def visitConditionParens(self, ctx:LuppoloParser.ConditionParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LuppoloParser#call.
    def visitCall(self, ctx:LuppoloParser.CallContext):
        return self.visitChildren(ctx)



del LuppoloParser