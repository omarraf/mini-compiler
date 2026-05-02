"""STUDENT 1 — Lexer tests."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lexer import Lexer, LexerError
from token_types import TokenType


def test_keywords():
    tokens = Lexer("int if else while").tokenize()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [TokenType.INT, TokenType.IF, TokenType.ELSE, TokenType.WHILE]


def test_operators():
    tokens = Lexer("+ - * / = == < >").tokenize()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [
        TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH,
        TokenType.ASSIGN, TokenType.EQ, TokenType.LT, TokenType.GT,
    ]


def test_number():
    tokens = Lexer("42").tokenize()
    tok = tokens[0]
    assert tok.type == TokenType.NUMBER
    assert tok.value == "42"


def test_identifier():
    tokens = Lexer("myVar").tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "myVar"


def test_invalid_char_raises():
    try:
        Lexer("@").tokenize()
        assert False, "Expected LexerError"
    except LexerError:
        pass


def test_line_tracking():
    tokens = Lexer("int\nx").tokenize()
    assert tokens[0].line == 1
    assert tokens[1].line == 2


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"  PASS  {name}")
            except Exception as e:
                print(f"  FAIL  {name}: {e}")
