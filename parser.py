"""
STUDENT 2 — Recursive Descent Parser + AST Construction

Responsibilities:
  - Accept the token list from the Lexer
  - Enforce TinyLang grammar rules (see grammar comment below)
  - Build and return a ProgramNode (the AST root)
  - Raise ParseError with a helpful message on invalid syntax

Grammar (BNF sketch — expand as needed):
  program       → statement* EOF
  statement     → var_decl | assign_stmt | if_stmt | while_stmt | block
  var_decl      → 'int' IDENTIFIER ';'
  assign_stmt   → IDENTIFIER '=' expression ';'
  if_stmt       → 'if' '(' expression ')' block ( 'else' block )?
  while_stmt    → 'while' '(' expression ')' block
  block         → '{' statement* '}'
  expression    → comparison
  comparison    → addition ( ('<' | '>' | '==') addition )*
  addition      → term ( ('+' | '-') term )*
  term          → factor ( ('*' | '/') factor )*
  factor        → NUMBER | IDENTIFIER | '(' expression ')'
"""

from token_types import Token, TokenType
from ast_nodes import (
    ProgramNode, VarDeclNode, AssignNode, BlockNode,
    IfNode, WhileNode, BinaryOpNode, NumberNode, IdentifierNode,
)


class ParseError(Exception):
    """Raised when the token stream violates the grammar."""


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0          # index of the current token

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def parse(self) -> ProgramNode:
        """Entry point. Parse a full program and return the AST root."""
        node = []
        while self._current().type != TokenType.EOF:
            node.append(self._parse_statement())
        return ProgramNode(statements=node)

    # ------------------------------------------------------------------
    # Statement parsers (one method per grammar rule)
    # ------------------------------------------------------------------

    def _parse_statement(self):
        """Dispatch to the correct statement parser based on current token."""
        if self._current().type == TokenType.INT:
            return self._parse_var_decl()
        if self._current().type == TokenType.IF:
            return self._parse_if()
        if self._current().type == TokenType.WHILE:
            return self._parse_while()
        if self._current().type == TokenType.LBRACE:
            return self._parse_block()
        if self._current().type == TokenType.IDENTIFIER:
            return self._parse_assign()
        else: raise ParseError(f"Unexpected token {self._current().type.name} on line {self._current().line} at start of statement")

    def _parse_var_decl(self) -> VarDeclNode:
        type_name = self._expect(TokenType.INT)
        var_name = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.SEMICOLON)
        return VarDeclNode(type_name=type_name.value, var_name=var_name.value, line=var_name.line) # use var_name for line number

    def _parse_assign(self) -> AssignNode:
        var_name = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.ASSIGN) #consume the '='
        value = self._parse_expression()
        self._expect(TokenType.SEMICOLON)
        return AssignNode(var_name=var_name.value, value=value, line=var_name.line)
        
    def _parse_if(self) -> IfNode:
        self._expect(TokenType.IF)
        self._expect(TokenType.LPAREN)
        condition = self._parse_expression()
        self._expect(TokenType.RPAREN)
        then_block = self._parse_block()
        if(self._match(TokenType.ELSE)):
            self._advance()
            else_block = self._parse_block()
        else:
            else_block = None

        return IfNode(condition=condition, then_block=then_block, else_block=else_block)

    def _parse_while(self) -> WhileNode:
        self._expect(TokenType.WHILE)
        self._expect(TokenType.LPAREN)
        condition = self._parse_expression()
        self._expect(TokenType.RPAREN)
        body = self._parse_block()
        return WhileNode(condition=condition, body=body)

    def _parse_block(self) -> BlockNode:
        self._expect(TokenType.LBRACE)
        statements = []
        while not self._match(TokenType.RBRACE, TokenType.EOF):
            statements.append(self._parse_statement())
        self._expect(TokenType.RBRACE)
        return BlockNode(statements)

    # ------------------------------------------------------------------
    # Expression parsers (ordered by precedence, lowest → highest)
    # ------------------------------------------------------------------

    def _parse_expression(self):
        """Lowest precedence — entry point for any expression."""
        return self._parse_comparison()

    def _parse_comparison(self):
        left = self._parse_addition()

        while self._match(TokenType.LT, TokenType.GT, TokenType.EQ):
            op = self._advance().value
            right = self._parse_addition()
            left = BinaryOpNode(op, left, right)

        return left
    

    def _parse_addition(self):
        left = self._parse_term()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._parse_term()
            left = BinaryOpNode(op, left, right)

        return left

    def _parse_term(self):
        left = self._parse_factor()

        while self._match(TokenType.STAR, TokenType.SLASH):
            op = self._advance().value
            right = self._parse_factor()
            left = BinaryOpNode(op, left, right)

        return left

    def _parse_factor(self):
        """Highest precedence: number, identifier, or parenthesized expression."""
        if self._match(TokenType.NUMBER):
            tok = self._advance()
            return NumberNode(value=int(tok.value))
        if self._match(TokenType.IDENTIFIER):
            tok = self._advance()
            return IdentifierNode(name=tok.value, line=tok.line)
        if self._match(TokenType.LPAREN):
            self._advance()
            node = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return node
        else: raise ParseError(f"Unexpected token {self._current().type.name} on line {self._current().line} in expression")

    # ------------------------------------------------------------------
    # Token navigation helpers
    # ------------------------------------------------------------------

    def _current(self) -> Token:
        """Return the token at self.pos without consuming it."""
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        """Consume and return the current token."""
        token = self.tokens[self.pos]
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def _expect(self, type: TokenType) -> Token:
        """
        Consume the current token if it matches `type`, otherwise raise ParseError.
        Use this for required grammar elements (keywords, punctuation).
        """
        if self._current().type == type: return self._advance()
        else: raise ParseError(f"Expected {type.name}, got {self._current().type.name} on line {self._current().line}")

    def _match(self, *types: TokenType) -> bool:
        """Return True (without consuming) if the current token is one of `types`."""
        return self._current().type in types
