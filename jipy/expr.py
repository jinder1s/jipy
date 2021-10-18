#!/usr/bin/env python3
from jipy.token import Token

from dataclasses import dataclass

@dataclass
class Expr:
    pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass
class Literal(Expr):
    value: object
