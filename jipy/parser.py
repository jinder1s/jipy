#!/usr/bin/env python3

from jipy.token_types import TokenTypes
from jipy.token import Token
from jipy.expr import Binary, Unary, Literal, Grouping


class Parser:

    def __init__(self, tokens: List[Token]):
        self._tokens = tuple(tokens)
        self._current = 0

    def match(self, *args: TokenTypes):
        for token_type in args:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, token_type: TokenTypes):
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self):
        if not self.is_at_end():
            self._current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == TokenTypes.EOF

    def peek(self):
        return self._tokens[self._current]

    def previous(self):
        return self._tokens[self._current - 1]

    def consume(self, token_type: TokenType, message: str):
        if self.check():
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        self.error_handler.error(token, message)
        return ParseError()

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparision()
        while self.match(TokenTypes.BANG_EQUAL, TokenTypes.EQUAL_EQUAL):
             operator = self.previous()
             right = self.comparision()
             expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenTypes.GREATER, TokenTypes.GREATER_EQUAL, TokenTypes.LESS, TokenTypes.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenTypes.MINUS, TokenTypes.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenTypes.SLASH, TokenTypes.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenTypes.BANG, TokenTypes.MINUS):
            operator = self.previous()
            right = self.unary(self)
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        expr = None # TODO: Check if returning a None is handled correctly
        if self.match(TokenTypes.FALSE):
            expr =  Literal(False)
        elif self.match(TokenTypes.TRUE):
            expr = Literal(True)
        elif self.match(TokenTypes.NIL):
            expr = Literal(None)
        elif self.match(TokenTypes.NUMBER, TokenTypes.STRING):
            expr = Literal(self.previous.literal)
        elif self.match(TokenTypes.LEFT_PAREN):
            sub_expr = self.expression()
            self.consume(TokenTypes.RIGHT_PAREN, "Expect ')' after expression.")
            expr = Grouping(sub_expr)
        return expr
