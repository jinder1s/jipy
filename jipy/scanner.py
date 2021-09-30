#!/usr/bin/env python3
"""Scanner for jipy language."""
from .token_types import TokenTypes
from .token import Token
from


class Scanner:
    def __init__(self, source):
        self.source = source

        self._start = 0
        self._current = 0
        self._line = 1

        self.tokens = []

    def is_end(self):
        return self._current == len(self.source)

    def advance(self):
        current += 1
        return self.source[current]

    def add_token(token_type, literal=None):
        text = self.source[self._start:self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))

    def scan_tokens(self):
        while not self.is_end():
            self._start = self._current
            self.scanToken();

        self.tokens.append(Token(TokenTypes.EOF, "", None, self._line)
        return self.tokens

    def scan_token(self):
        character = self.advance()
        if character == '(':
            self.add_token(TokenTypes.LEFT_PAREN)
        elif character == ')':
            self.add_token(TokenTypes.RIGHT_PAREN)
        elif character == '{':
            self.add_token(TokenTypes.LEFT_BRACE)
        elif character == '}':
            self.add_token(TokenTypes.RIGHT_BRACE)
        elif character == ',':
            self.add_token(TokenTypes.COMMA)
        elif character == '.':
            self.add_token(TokenTypes.DOT)
        elif character == '-':
            self.add_token(TokenTypes.MINUS)
        elif character == '+':
            self.add_token(TokenTypes.PLUS)
        elif character == ';':
            self.add_token(TokenTypes.SEMICOLON)
        elif character == '*':
            self.add_token(TokenTypes.STAR)
