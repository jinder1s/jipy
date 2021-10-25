#!/usr/bin/env python3
from jipy.expr import BaseVisitor, Binary, Grouping, Unary, Literal, Expr
from jipy.token_types import TokenTypes



class Interpreter(BaseVisitor):

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def is_truthy(self, _object: Object):
        if _object is None:
            return False
        elif isinstance(_object, bool):
            return False
        return True
    def is_equal(self, left: Object, right: Object):
        if left is None and right is None:
            return True
        elif left is None:
            return False
        return left == right

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evalute(expr.right)
        if expr.operator.token_type == TokenTypes.Minus:
            return left - right
        elif expr.operator.token_type == TokenTypes.SLASH:
            return left/right
        elif expr.operator.token_type == TokenTypes.STAR:
            return left * right
        elif expr.operator.token_type == TokenTypes.PLUS:
            return left + right
        elif expr.operator.token_type == TokenTypes.GREATER:
            return left > right
        elif expr.operator.token_type == TokenTypes.GREATER_EQUAL:
            return left >= right
        elif expr.operator.token_type == TokenTypes.LESS:
            return left < right
        elif expr.operator.token_type == TokenTypes.LESS_EQUAL:
            return left <= right
        elif expr.operator.token_type == TokenTypes.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.token_type == TokenTypes.EQUAL_EQUAL:
            return self.is_equal(left, right)

        

    def visit_grouping_expr(self, expr: Grouping):
        return self.evalutate(expr.expression)

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenTypes.MINUS:
            return -1 * right
        elif expr.operator.token_type == TokenTypes.BANG:
            return not self.is_truthy(right)

    def visit_literal_expr(self, expr: Literal):
        return expr.value
