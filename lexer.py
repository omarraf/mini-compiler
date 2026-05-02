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
        self.pos = 0          # current character index
        self.line = 1         # current line number (for error messages)

    # ------------------------------------------------------------------
    # Public interface (called by main.py)
    # ------------------------------------------------------------------

    def tokenize(self) -> list[Token]:
        """
        Scan the entire source and return a flat list of Tokens.
        The last token must be Token(EOF, '', ...).

        Steps to implement:
          1. Skip whitespace (increment self.line on newlines)
          2. Skip single-line comments if you add them (// ...)
          3. Match multi-char tokens first (==) before single-char (=)
          4. Match numbers (consecutive digits)
          5. Match identifiers/keywords (letter/underscore followed by alphanum)
          6. Match single-char operators and delimiters
          7. Raise LexerError for anything else
        """
        # TODO: create an empty list to collect tokens
        # TODO: loop while self._current() != '':
        #           call self._skip_whitespace()
        #           if _current() is a digit        → append self._read_number()
        #           elif _current() is alpha/_       → append self._read_identifier_or_keyword()
        #           elif _current() == '=' and _peek() == '=' → _advance() twice, append EQ token
        #           elif _current() in single-char map       → _advance(), append matching token
        #           else                                      → raise LexerError
        # TODO: append Token(TokenType.EOF, '', self.line)
        # TODO: return the list
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Helper methods (implement as needed)
    # ------------------------------------------------------------------

    def _current(self) -> str:
        """Return the character at self.pos, or '' if past end."""
        # TODO: return self.source[self.pos] if self.pos < len(self.source) else ''
        raise NotImplementedError

    def _advance(self) -> str:
        """Consume and return the current character, advancing self.pos."""
        # TODO: save self.source[self.pos], increment self.pos, return saved char
        raise NotImplementedError

    def _peek(self) -> str:
        """Return the character after the current one without consuming it."""
        # TODO: return self.source[self.pos + 1] if self.pos + 1 < len(self.source) else ''
        raise NotImplementedError

    def _skip_whitespace(self) -> None:
        """Advance past spaces, tabs, and newlines; track self.line."""
        # TODO: while _current() in (' ', '\t', '\r', '\n'):
        #           if _current() == '\n': self.line += 1
        #           self._advance()
        raise NotImplementedError

    def _read_number(self) -> Token:
        """Consume consecutive digit characters and return a NUMBER token."""
        # TODO: record start line
        # TODO: build up a string by calling _advance() while _current().isdigit()
        # TODO: return Token(TokenType.NUMBER, collected_string, start_line)
        raise NotImplementedError

    def _read_identifier_or_keyword(self) -> Token:
        """
        Consume an identifier (letter/underscore + alphanum).
        Return a keyword TokenType if the text is in KEYWORDS, else IDENTIFIER.
        """
        # TODO: record start line
        # TODO: build up a string while _current().isalnum() or _current() == '_'
        # TODO: look up text in KEYWORDS dict → get token type (default IDENTIFIER)
        # TODO: return Token(token_type, text, start_line)
        raise NotImplementedError
