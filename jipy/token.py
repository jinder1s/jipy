#!/usr/bin/env python3


class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self):
        return f"{self.token_type}: {self.lexeme} {self.literal}"

    def __repr__(self):
        return self.to_string()
