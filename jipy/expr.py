#!/usr/bin/env python3

from abc import ABC, abstractmethod
from dataclasses import dataclass

from jipy.token import Token


@dataclass
class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        return NotImplemented


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class BaseVisitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        return NotImplemented

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        return NotImplemented

    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        return NotImplemented

    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        return NotImplemented
