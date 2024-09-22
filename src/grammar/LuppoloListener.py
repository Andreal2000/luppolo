# Generated from Luppolo.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .LuppoloParser import LuppoloParser
else:
    from LuppoloParser import LuppoloParser

# This class defines a complete listener for a parse tree produced by LuppoloParser.
class LuppoloListener(ParseTreeListener):

    # Enter a parse tree produced by LuppoloParser#program.
    def enterProgram(self, ctx:LuppoloParser.ProgramContext):
        pass

    # Exit a parse tree produced by LuppoloParser#program.
    def exitProgram(self, ctx:LuppoloParser.ProgramContext):
        pass


    # Enter a parse tree produced by LuppoloParser#function.
    def enterFunction(self, ctx:LuppoloParser.FunctionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#function.
    def exitFunction(self, ctx:LuppoloParser.FunctionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#block.
    def enterBlock(self, ctx:LuppoloParser.BlockContext):
        pass

    # Exit a parse tree produced by LuppoloParser#block.
    def exitBlock(self, ctx:LuppoloParser.BlockContext):
        pass


    # Enter a parse tree produced by LuppoloParser#declarationInstruction.
    def enterDeclarationInstruction(self, ctx:LuppoloParser.DeclarationInstructionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#declarationInstruction.
    def exitDeclarationInstruction(self, ctx:LuppoloParser.DeclarationInstructionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#foreachInstruction.
    def enterForeachInstruction(self, ctx:LuppoloParser.ForeachInstructionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#foreachInstruction.
    def exitForeachInstruction(self, ctx:LuppoloParser.ForeachInstructionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#ifElseInstruction.
    def enterIfElseInstruction(self, ctx:LuppoloParser.IfElseInstructionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#ifElseInstruction.
    def exitIfElseInstruction(self, ctx:LuppoloParser.IfElseInstructionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#ifInstruction.
    def enterIfInstruction(self, ctx:LuppoloParser.IfInstructionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#ifInstruction.
    def exitIfInstruction(self, ctx:LuppoloParser.IfInstructionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#repeatInstruction.
    def enterRepeatInstruction(self, ctx:LuppoloParser.RepeatInstructionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#repeatInstruction.
    def exitRepeatInstruction(self, ctx:LuppoloParser.RepeatInstructionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#returnInstruction.
    def enterReturnInstruction(self, ctx:LuppoloParser.ReturnInstructionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#returnInstruction.
    def exitReturnInstruction(self, ctx:LuppoloParser.ReturnInstructionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#whileInstruction.
    def enterWhileInstruction(self, ctx:LuppoloParser.WhileInstructionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#whileInstruction.
    def exitWhileInstruction(self, ctx:LuppoloParser.WhileInstructionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#nat.
    def enterNat(self, ctx:LuppoloParser.NatContext):
        pass

    # Exit a parse tree produced by LuppoloParser#nat.
    def exitNat(self, ctx:LuppoloParser.NatContext):
        pass


    # Enter a parse tree produced by LuppoloParser#callExpression.
    def enterCallExpression(self, ctx:LuppoloParser.CallExpressionContext):
        pass

    # Exit a parse tree produced by LuppoloParser#callExpression.
    def exitCallExpression(self, ctx:LuppoloParser.CallExpressionContext):
        pass


    # Enter a parse tree produced by LuppoloParser#sym.
    def enterSym(self, ctx:LuppoloParser.SymContext):
        pass

    # Exit a parse tree produced by LuppoloParser#sym.
    def exitSym(self, ctx:LuppoloParser.SymContext):
        pass


    # Enter a parse tree produced by LuppoloParser#expressionParens.
    def enterExpressionParens(self, ctx:LuppoloParser.ExpressionParensContext):
        pass

    # Exit a parse tree produced by LuppoloParser#expressionParens.
    def exitExpressionParens(self, ctx:LuppoloParser.ExpressionParensContext):
        pass


    # Enter a parse tree produced by LuppoloParser#pow.
    def enterPow(self, ctx:LuppoloParser.PowContext):
        pass

    # Exit a parse tree produced by LuppoloParser#pow.
    def exitPow(self, ctx:LuppoloParser.PowContext):
        pass


    # Enter a parse tree produced by LuppoloParser#addSub.
    def enterAddSub(self, ctx:LuppoloParser.AddSubContext):
        pass

    # Exit a parse tree produced by LuppoloParser#addSub.
    def exitAddSub(self, ctx:LuppoloParser.AddSubContext):
        pass


    # Enter a parse tree produced by LuppoloParser#unary.
    def enterUnary(self, ctx:LuppoloParser.UnaryContext):
        pass

    # Exit a parse tree produced by LuppoloParser#unary.
    def exitUnary(self, ctx:LuppoloParser.UnaryContext):
        pass


    # Enter a parse tree produced by LuppoloParser#id.
    def enterId(self, ctx:LuppoloParser.IdContext):
        pass

    # Exit a parse tree produced by LuppoloParser#id.
    def exitId(self, ctx:LuppoloParser.IdContext):
        pass


    # Enter a parse tree produced by LuppoloParser#mulDiv.
    def enterMulDiv(self, ctx:LuppoloParser.MulDivContext):
        pass

    # Exit a parse tree produced by LuppoloParser#mulDiv.
    def exitMulDiv(self, ctx:LuppoloParser.MulDivContext):
        pass


    # Enter a parse tree produced by LuppoloParser#not.
    def enterNot(self, ctx:LuppoloParser.NotContext):
        pass

    # Exit a parse tree produced by LuppoloParser#not.
    def exitNot(self, ctx:LuppoloParser.NotContext):
        pass


    # Enter a parse tree produced by LuppoloParser#comparison.
    def enterComparison(self, ctx:LuppoloParser.ComparisonContext):
        pass

    # Exit a parse tree produced by LuppoloParser#comparison.
    def exitComparison(self, ctx:LuppoloParser.ComparisonContext):
        pass


    # Enter a parse tree produced by LuppoloParser#boolean.
    def enterBoolean(self, ctx:LuppoloParser.BooleanContext):
        pass

    # Exit a parse tree produced by LuppoloParser#boolean.
    def exitBoolean(self, ctx:LuppoloParser.BooleanContext):
        pass


    # Enter a parse tree produced by LuppoloParser#or.
    def enterOr(self, ctx:LuppoloParser.OrContext):
        pass

    # Exit a parse tree produced by LuppoloParser#or.
    def exitOr(self, ctx:LuppoloParser.OrContext):
        pass


    # Enter a parse tree produced by LuppoloParser#and.
    def enterAnd(self, ctx:LuppoloParser.AndContext):
        pass

    # Exit a parse tree produced by LuppoloParser#and.
    def exitAnd(self, ctx:LuppoloParser.AndContext):
        pass


    # Enter a parse tree produced by LuppoloParser#conditionParens.
    def enterConditionParens(self, ctx:LuppoloParser.ConditionParensContext):
        pass

    # Exit a parse tree produced by LuppoloParser#conditionParens.
    def exitConditionParens(self, ctx:LuppoloParser.ConditionParensContext):
        pass


    # Enter a parse tree produced by LuppoloParser#call.
    def enterCall(self, ctx:LuppoloParser.CallContext):
        pass

    # Exit a parse tree produced by LuppoloParser#call.
    def exitCall(self, ctx:LuppoloParser.CallContext):
        pass



del LuppoloParser