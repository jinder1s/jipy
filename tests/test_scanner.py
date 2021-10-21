#!/usr/bin/env python3

import pytest
from unittest import TestCase
from unittest.mock import Mock
from jipy.token_types import TokenTypes
from jipy.scanner import Scanner


@pytest.mark.parametrize(
    "current,length",
    [(0, 0), (0, 10), (5, 10), (10, 10)],
)
def test_is_end(current, length):
    """Checks to make sure is_end only returns True when self._current == len of input"""
    scanner = Scanner("=" * length)
    scanner._current = current
    if current == length:
        assert scanner.is_end() == True
    else:
        assert scanner.is_end() == False


@pytest.mark.parametrize("current", [0, 1, 3, 5])
def test_advance(current):
    """Test to make sure advance returns the value at the current iterator"""
    source = "abcdefghijklmno"
    scanner = Scanner(source)
    scanner._current = current
    returned_char = scanner.advance()
    assert returned_char == source[current]
    assert scanner._current == current + 1


@pytest.mark.parametrize(
    "current,input_val, source, result",
    [
        (0, "1", "1234", True),
        (5, "6", "1234567", True),
        (5, "7", "1234567", False),  # False cause checks wrong velue
        (6, "", "234234567", False),  # False cause empty expected_char
        (4, "7", "1234", False),  # False cause is at end
    ],
)
def test_match(current, input_val, source, result):
    """Test to make sure advance returns the value at the current iterator"""
    scanner = Scanner(source)
    scanner._current = current
    assert scanner.match(input_val) is result


@pytest.mark.parametrize(
    "current, source, expected",
    [
        (0, "abc", "a"),
        (2, "abc", "c"),
        (3, "abc", "\0"),
    ],
)
def test_peek(current, source, expected):
    scanner = Scanner(source)
    scanner._current = current
    assert scanner.peek() == expected


@pytest.mark.parametrize(
    "current, source, expected",
    [
        (0, "abc", "b"),
        (1, "abc", "c"),
        (2, "abc", "\0"),
        (3, "abc", "\0"),
    ],
)
def test_peek_next(current, source, expected):
    scanner = Scanner(source)
    scanner._current = current
    assert scanner.peek_next() == expected


@pytest.mark.parametrize(
    "token_type, lexeme, current",
    [
        (TokenTypes.LEFT_PAREN, "(", 5),
        (TokenTypes.LEFT_BRACE, "{", 7),
        (TokenTypes.DOT, ".", 2),
    ],
)
def test_add_token(token_type, lexeme, current):
    """Makes sure add_token takes the current lexemes from source and adds correct token_type"""
    # TODO: Add examples for longer tokens
    source = "+++==++==++"
    source = source[:current] + lexeme + source[current:]

    scanner = Scanner(source)
    scanner._start = current
    scanner._current = current + 1

    scanner.add_token(token_type)

    assert len(scanner.tokens) == 1
    assert scanner.tokens[0].token_type == token_type


@pytest.mark.parametrize(
    "num,expected", [("1", True), ("0", True), ("a", False), ("\n", False)]
)
def test_is_digit(num, expected):
    scanner = Scanner("")
    assert scanner.is_digit(num) == expected


@pytest.mark.parametrize(
    "char,expected", [("a", True), ("d", True), ("1", False), ("\n", False)]
)
def test_is_alpha(char, expected):
    scanner = Scanner("")
    assert scanner.is_alpha(char) == expected


@pytest.mark.parametrize(
    "char,expected",
    [("a", True), ("d", True), ("1", True), ("\n", False), (";", False), (".", False)],
)
def test_is_alpha_numeric(char, expected):
    scanner = Scanner("")
    assert scanner.is_alpha_numeric(char) == expected


@pytest.mark.parametrize(
    "token_type, lexeme",
    [(TokenTypes.LEFT_PAREN, "("), (TokenTypes.LEFT_BRACE, "{"), (TokenTypes.DOT, ".")],
)
def test_scan_token_one_char(token_type, lexeme):
    """Make sure scan_token scans correctly and adds to self.tokens list"""
    scanner = Scanner("sdfs")
    scanner.add_token = Mock()
    scanner.advance = Mock()
    scanner.advance.return_value = lexeme

    scanner.scan_token()

    scanner.add_token.assert_called_with(token_type)
    scanner.add_token.assert_called_once()


@pytest.mark.parametrize(
    "token_type, lexeme",
    [
        (TokenTypes.BANG_EQUAL, "!="),
        (TokenTypes.BANG, "!"),
        (TokenTypes.LESS_EQUAL, "<="),
        (TokenTypes.LESS, "<"),
        (TokenTypes.GREATER_EQUAL, ">="),
        (TokenTypes.GREATER, ">"),
        (TokenTypes.EQUAL_EQUAL, "=="),
        (TokenTypes.EQUAL, "="),
    ],
)
def test_scan_token_two_char(token_type, lexeme):
    """Make sure scan_token scans correctly and adds to self.tokens list"""
    scanner = Scanner("sdfs")
    scanner.add_token = Mock()
    scanner.advance = Mock()
    scanner.advance.return_value = lexeme[0]

    def match_side_effect(expected_val):
        if len(lexeme) == 2 and expected_val == lexeme[1]:
            return True
        return False

    scanner.match = Mock()
    scanner.match.side_effect = match_side_effect

    scanner.scan_token()

    scanner.add_token.assert_called_with(token_type)
    scanner.add_token.assert_called_once()


@pytest.mark.parametrize(
    "source, token_types",
    [
        ("//blah \n", [TokenTypes.EOF]),
        ("123.01", [TokenTypes.NUMBER, TokenTypes.EOF]),
        ('"abcd"', [TokenTypes.STRING, TokenTypes.EOF]),
        ("if", [TokenTypes.IF, TokenTypes.EOF]),
        ("iffor", [TokenTypes.IDENTIFIER, TokenTypes.EOF]),
        ("if,for", [TokenTypes.IF, TokenTypes.COMMA, TokenTypes.FOR, TokenTypes.EOF]),
        ("blah", [TokenTypes.IDENTIFIER, TokenTypes.EOF]),
        ("blah\nohno", [TokenTypes.IDENTIFIER, TokenTypes.IDENTIFIER, TokenTypes.EOF]),
        ("blah_1_sd", [TokenTypes.IDENTIFIER, TokenTypes.EOF]),
        (
            '(blah = "hi")',
            [
                TokenTypes.LEFT_PAREN,
                TokenTypes.IDENTIFIER,
                TokenTypes.EQUAL,
                TokenTypes.STRING,
                TokenTypes.RIGHT_PAREN,
                TokenTypes.EOF,
            ],
        ),
        (
            "( a = 1)",
            [
                TokenTypes.LEFT_PAREN,
                TokenTypes.IDENTIFIER,
                TokenTypes.EQUAL,
                TokenTypes.NUMBER,
                TokenTypes.RIGHT_PAREN,
                TokenTypes.EOF,
            ],
        ),
    ],
)
def test_scan_tokens_simple(source, token_types):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for i, token in enumerate(tokens):
        assert token.token_type == token_types[i]


def test_scan_tokens_parens():
    """Make sure a group of parens are scan correctly"""
    code = "(((())))"
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    assert len(tokens) == len(code) + 1
    assert tokens[-1].token_type == TokenTypes.EOF
    assert tokens[0].token_type == TokenTypes.LEFT_PAREN
    assert tokens[1].token_type == TokenTypes.LEFT_PAREN
    assert tokens[2].token_type == TokenTypes.LEFT_PAREN
    assert tokens[3].token_type == TokenTypes.LEFT_PAREN
    assert tokens[4].token_type == TokenTypes.RIGHT_PAREN
    assert tokens[5].token_type == TokenTypes.RIGHT_PAREN
    assert tokens[6].token_type == TokenTypes.RIGHT_PAREN
    assert tokens[7].token_type == TokenTypes.RIGHT_PAREN


def test_scan_tokens_empty_input():
    scanner = Scanner("")
    tokens = scanner.scan_tokens()
    assert len(tokens) == 1
    assert tokens[0].token_type == TokenTypes.EOF
