#!/usr/bin/env python3


class Token:
    def __init__(token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self):
        return f"{self.token_type}: {self.lexeme} {self.literal}"
