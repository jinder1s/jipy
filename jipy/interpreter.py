#!/usr/bin/env python3
from typing import List, Any
from jipy.expr import BaseVisitor, Binary, Grouping, Unary, Literal, Expr
from jipy.token_types import TokenTypes
from jipy.token import Token
from jipy.error import RunTimeError, JipyError



class Interpreter(BaseVisitor):

    def interpret(self, expression: Expr):
        try:
            value = self.evaluate(expression)
            print(value)
            breakpoint()
        except RunTimeError as err:
            JipyError.run_time_error(err)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def is_truthy(self, _object: Any):
        if _object is None:
            return False
        elif isinstance(_object, bool):
            return False
        return True

    def is_equal(self, left: Any, right: Any):
        if left is None and right is None:
            return True
        elif left is None:
            return False
        return left == right

    def check_if_number(self, operator: Token, *operands: List[Any]):

        is_not_number =  [ type(operand) != int and type(operand) != float for operand in operands]
        if any(is_not_number):
            raise RunTimeError(operator, "Operand must be a number, is type")


    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenTypes.MINUS:
            self.check_if_number(expr.operator, left, right)
            return left - right
        elif expr.operator.token_type == TokenTypes.SLASH:
            self.check_if_number(expr.operator, left, right)
            return left/right
        elif expr.operator.token_type == TokenTypes.STAR:
            self.check_if_number(expr.operator, left, right)
            return left * right
        elif expr.operator.token_type == TokenTypes.PLUS:
            if type(left) in [int, float, str] or type(right) in [int, float, str]:
                return left + right
            raise RunTimeError(expr.operator, "Operansd must be two numbers or two strings")
        elif expr.operator.token_type == TokenTypes.GREATER:
            self.check_if_number(expr.operator, left, right)
            return left > right
        elif expr.operator.token_type == TokenTypes.GREATER_EQUAL:
            self.check_if_number(expr.operator, left, right)
            return left >= right
        elif expr.operator.token_type == TokenTypes.LESS:
            self.check_if_number(expr.operator, left, right)
            return left < right
        elif expr.operator.token_type == TokenTypes.LESS_EQUAL:
            self.check_if_number(expr.operator, left, right)
            return left <= right
        elif expr.operator.token_type == TokenTypes.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.token_type == TokenTypes.EQUAL_EQUAL:
            return self.is_equal(left, right)

        

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenTypes.MINUS:
            self.check_if_number(expr.operator, right)
            return -1 * right
        elif expr.operator.token_type == TokenTypes.BANG:
            return not self.is_truthy(right)

    def visit_literal_expr(self, expr: Literal):
        return expr.value
