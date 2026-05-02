"""
STUDENT 1 — Token definitions shared across the pipeline.
Define all token types here so lexer.py, parser.py, and the rest can import them.
"""

from enum import Enum, auto


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    IDENTIFIER = auto()

    # Keywords
    INT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()       # =
    EQ = auto()           # ==
    LT = auto()           # <
    GT = auto()           # >

    # Delimiters
    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()

    # Control
    EOF = auto()


# Maps keyword strings → their TokenType so the lexer can look them up
KEYWORDS: dict[str, TokenType] = {
    "int":   TokenType.INT,
    "if":    TokenType.IF,
    "else":  TokenType.ELSE,
    "while": TokenType.WHILE,
}


class Token:
    """A single lexical token."""

    def __init__(self, type: TokenType, value: str, line: int):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line})"
