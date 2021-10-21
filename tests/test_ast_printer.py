import pytest
from jipy.ast_printer import AstPrinter
from jipy.token import Token
from jipy.token_types import TokenTypes
from jipy.expr import Binary, Unary, Grouping, Literal


def test_binary_expression():
    ast_printer = AstPrinter()
    expr = Binary(Literal(1), Token(TokenTypes.STAR, "*", None, 1), Literal(2))
    assert ast_printer.print(expr) == "(* 1 2)"


def test_unary_expression():
    ast_printer = AstPrinter()
    expr = Unary(Token(TokenTypes.STAR, "*", None, 1), Literal(2))
    assert ast_printer.print(expr) == "(* 2)"


def test_complex_expression():
    ast_printer = AstPrinter()
    expr = Binary(
        Unary(Token(TokenTypes.STAR, "*", None, 1), Literal(3)),
        Token(TokenTypes.STAR, "*", None, 1),
        Literal(2),
    )
    assert ast_printer.print(expr) == "(* (* 3) 2)"
