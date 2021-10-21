#!/usr/bin/env python3
"""Scanner for jipy language."""
from jipy.token_types import TokenTypes
from jipy.token import Token
from jipy.error import JipyError


class Scanner:
    SINGLE_CHAR_TOKENS = {
        "(": TokenTypes.LEFT_PAREN,
        ")": TokenTypes.RIGHT_PAREN,
        "{": TokenTypes.LEFT_BRACE,
        "}": TokenTypes.RIGHT_BRACE,
        ",": TokenTypes.COMMA,
        ".": TokenTypes.DOT,
        "-": TokenTypes.MINUS,
        "+": TokenTypes.PLUS,
        ";": TokenTypes.SEMICOLON,
        "*": TokenTypes.STAR,
    }

    TWO_CHAR_TOKENS = {
        "!": ("=", TokenTypes.BANG_EQUAL, TokenTypes.BANG),
        "<": ("=", TokenTypes.LESS_EQUAL, TokenTypes.LESS),
        ">": ("=", TokenTypes.GREATER_EQUAL, TokenTypes.GREATER),
        "=": ("=", TokenTypes.EQUAL_EQUAL, TokenTypes.EQUAL),
        # "=": {"": TokenTypes.EQUAL,
        #       "=": TokenTypes.EQUAL_EQUAL,
        #       },
        # "<": {""}
    }
    MEANINGLESS_CHARACTERS = (" ", "\r", "\t")

    RESERVED_WORDS = {
        "and": TokenTypes.AND,
        "class": TokenTypes.CLASS,
        "else": TokenTypes.ELSE,
        "false": TokenTypes.FALSE,
        "for": TokenTypes.FOR,
        "fun": TokenTypes.FUNCTION,
        "if": TokenTypes.IF,
        "nil": TokenTypes.NIL,
        "or": TokenTypes.OR,
        "print": TokenTypes.PRINT,
        "return": TokenTypes.RETURN,
        "super": TokenTypes.SUPER,
        "this": TokenTypes.THIS,
        "true": TokenTypes.TRUE,
        "var": TokenTypes.VAR,
        "while": TokenTypes.WHILE,
    }

    def __init__(self, source):
        self.source = source

        self._start = 0
        self._current = 0
        self._line = 1

        self.tokens = []

    def is_end(self):
        return self._current == len(self.source)

    def advance(self):
        character = self.source[self._current]
        self._current += 1
        return character

    def peek(self):
        if self.is_end():
            return "\0"
        return self.source[self._current]

    def peek_next(self):
        if self._current + 1 >= len(self.source):
            return "\0"
        return self.source[self._current + 1]

    def match(self, expected_char):
        if self.is_end() or not expected_char:
            return False
        if self.source[self._current] != expected_char:
            return False
        self._current += 1
        return True

    def add_token(self, token_type, literal=None):
        text = self.source[self._start : self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))

    def scan_tokens(self):
        while not self.is_end():
            self._start = self._current
            self.scan_token()

        self.tokens.append(Token(TokenTypes.EOF, "", None, self._line))
        return self.tokens

    def scan_token(self):
        character = self.advance()
        if character in self.SINGLE_CHAR_TOKENS:
            self.add_token(self.SINGLE_CHAR_TOKENS[character])
        elif character in self.TWO_CHAR_TOKENS:
            possible_token = self.TWO_CHAR_TOKENS[character]
            if self.match(possible_token[0]):
                self.add_token(possible_token[1])
            else:
                self.add_token(possible_token[2])
        elif self.is_alpha(character):
            self.identifier()
        elif self.is_digit(character):
            self.number()
        elif character == '"':
            self.string()
        elif character == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_end():
                    self.advance()
            else:
                self.add_token(TokenTypes.SLASH)
        elif character in self.MEANINGLESS_CHARACTERS:
            pass
        elif character == "\n":
            self._line += 1
        else:
            print(f"invalid charater '{character}'")

    def string(self):
        while self.peek() != '"' and not self.is_end():
            if self.peek() == "\n":
                self._line += 1
            self.advance()

        if self.is_end():
            # TODO: figure out what to do about errors
            JipyError.report(self._line, "", "Unterminated string")

        self.advance()

        string_value = self.source[self._start + 1 : self._current - 1]

        self.add_token(TokenTypes.STRING, string_value)

    def is_digit(self, char):
        return '0' <= char <= "9"

    def is_alpha(self, char):
        return "a" <= char <= "z" or "A" <= char <= "Z" or char == "_"

    def is_alpha_numeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

        while self.is_digit(self.peek()):
            self.advance()

        self.add_token(
            TokenTypes.NUMBER, float(self.source[self._start : self._current])
        )

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self._start : self._current]
        identifier_type = self.RESERVED_WORDS.get(text, None)
        if identifier_type is None:
            identifier_type = TokenTypes.IDENTIFIER
        self.add_token(identifier_type)
