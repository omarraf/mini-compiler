"""
STUDENT 1 — Lexical Analyzer (Scanner)

Responsibilities:
  - Walk the source string character-by-character
  - Emit a Token for each recognized lexeme
  - Raise LexerError on unrecognized characters
  - Output a complete token stream (list of Tokens ending with EOF)
"""

from token_types import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """Raised when an unrecognized character is encountered."""


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1

    # ------------------------------------------------------------------
    # Public interface (called by main.py)
    # ------------------------------------------------------------------

    def tokenize(self) -> list[Token]:
        tokens = []

        while self._current() != '':
            self._skip_whitespace()

            ch = self._current()

            if ch == '':
                break
            elif ch.isdigit():
                tokens.append(self._read_number())
            elif ch.isalpha() or ch == '_':
                tokens.append(self._read_identifier_or_keyword())
            elif ch == '=' and self._peek() == '=':
                self._advance()
                self._advance()
                tokens.append(Token(TokenType.EQ, '==', self.line))
            else:
                single = {
                    '=': TokenType.ASSIGN,
                    '+': TokenType.PLUS,
                    '-': TokenType.MINUS,
                    '*': TokenType.STAR,
                    '/': TokenType.SLASH,
                    '<': TokenType.LT,
                    '>': TokenType.GT,
                    ';': TokenType.SEMICOLON,
                    '(': TokenType.LPAREN,
                    ')': TokenType.RPAREN,
                    '{': TokenType.LBRACE,
                    '}': TokenType.RBRACE,
                }
                if ch in single:
                    tokens.append(Token(single[ch], ch, self.line))
                    self._advance()
                else:
                    raise LexerError(f"Unexpected character '{ch}' on line {self.line}")

        tokens.append(Token(TokenType.EOF, '', self.line))
        return tokens

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _current(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else ''

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        return ch

    def _peek(self) -> str:
        next_pos = self.pos + 1
        return self.source[next_pos] if next_pos < len(self.source) else ''

    def _skip_whitespace(self) -> None:
        while self._current() in (' ', '\t', '\r', '\n'):
            if self._current() == '\n':
                self.line += 1
            self._advance()

    def _read_number(self) -> Token:
        start_line = self.line
        text = ''
        while self._current().isdigit():
            text += self._advance()
        return Token(TokenType.NUMBER, text, start_line)

    def _read_identifier_or_keyword(self) -> Token:
        start_line = self.line
        text = ''
        while self._current().isalnum() or self._current() == '_':
            text += self._advance()
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        return Token(token_type, text, start_line)
