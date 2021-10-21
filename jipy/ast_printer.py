#!/usr/bin/env python3
from typing import List
from jipy.expr import BaseVisitor, Expr, Binary, Grouping, Unary, Literal


class AstPrinter(BaseVisitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, exprs: List[Expr]):
        expr_repr = [expr.accept(self) for expr in exprs]
        return f'({name} {" ".join(expr_repr)})'

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", [expr.expression])

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, [expr.right])

    def visit_literal_expr(self, expr: Literal):
        return str(expr.value)
