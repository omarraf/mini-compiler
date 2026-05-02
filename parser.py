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
        # TODO: create a ProgramNode
        # TODO: loop calling _parse_statement() until _current().type == EOF
        # TODO: return the ProgramNode
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Statement parsers (one method per grammar rule)
    # ------------------------------------------------------------------

    def _parse_statement(self):
        """Dispatch to the correct statement parser based on current token."""
        # TODO: if current token is INT      → return _parse_var_decl()
        # TODO: if current token is IF       → return _parse_if()
        # TODO: if current token is WHILE    → return _parse_while()
        # TODO: if current token is LBRACE   → return _parse_block()
        # TODO: if current token is IDENTIFIER → return _parse_assign()
        # TODO: else raise ParseError with the unexpected token info
        raise NotImplementedError

    def _parse_var_decl(self) -> VarDeclNode:
        # TODO: _expect(INT) to consume 'int'
        # TODO: _expect(IDENTIFIER) to get the variable name token
        # TODO: _expect(SEMICOLON)
        # TODO: return VarDeclNode(type_name='int', var_name=<name token>.value, line=...)
        raise NotImplementedError

    def _parse_assign(self) -> AssignNode:
        # TODO: _expect(IDENTIFIER) to get the variable name token
        # TODO: _expect(ASSIGN) to consume '='
        # TODO: call _parse_expression() to get the value node
        # TODO: _expect(SEMICOLON)
        # TODO: return AssignNode(var_name=..., value=..., line=...)
        raise NotImplementedError

    def _parse_if(self) -> IfNode:
        # TODO: _expect(IF)
        # TODO: _expect(LPAREN)
        # TODO: parse condition with _parse_expression()
        # TODO: _expect(RPAREN)
        # TODO: parse then_block with _parse_block()
        # TODO: if _match(ELSE): _advance(), parse else_block with _parse_block()
        # TODO: return IfNode(condition=..., then_block=..., else_block=...)
        raise NotImplementedError

    def _parse_while(self) -> WhileNode:
        # TODO: _expect(WHILE)
        # TODO: _expect(LPAREN)
        # TODO: parse condition with _parse_expression()
        # TODO: _expect(RPAREN)
        # TODO: parse body with _parse_block()
        # TODO: return WhileNode(condition=..., body=...)
        raise NotImplementedError

    def _parse_block(self) -> BlockNode:
        # TODO: _expect(LBRACE)
        # TODO: collect statements in a list, loop until current token is RBRACE or EOF
        # TODO: _expect(RBRACE)
        # TODO: return BlockNode(statements=[...])
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Expression parsers (ordered by precedence, lowest → highest)
    # ------------------------------------------------------------------

    def _parse_expression(self):
        """Lowest precedence — entry point for any expression."""
        # TODO: just delegate to _parse_comparison() for now
        raise NotImplementedError

    def _parse_comparison(self):
        # TODO: call _parse_addition() to get left side
        # TODO: while _match(LT, GT, EQ):
        #           save op = _advance().value
        #           right = _parse_addition()
        #           left = BinaryOpNode(op, left, right)
        # TODO: return left
        raise NotImplementedError

    def _parse_addition(self):
        # TODO: call _parse_term() to get left side
        # TODO: while _match(PLUS, MINUS):
        #           save op = _advance().value
        #           right = _parse_term()
        #           left = BinaryOpNode(op, left, right)
        # TODO: return left
        raise NotImplementedError

    def _parse_term(self):
        # TODO: call _parse_factor() to get left side
        # TODO: while _match(STAR, SLASH):
        #           save op = _advance().value
        #           right = _parse_factor()
        #           left = BinaryOpNode(op, left, right)
        # TODO: return left
        raise NotImplementedError

    def _parse_factor(self):
        """Highest precedence: number, identifier, or parenthesized expression."""
        # TODO: if _match(NUMBER)     → tok = _advance(), return NumberNode(int(tok.value))
        # TODO: if _match(IDENTIFIER) → tok = _advance(), return IdentifierNode(tok.value, tok.line)
        # TODO: if _match(LPAREN)     → _advance(), node = _parse_expression(), _expect(RPAREN), return node
        # TODO: else raise ParseError (unexpected token)
        raise NotImplementedError

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
        # TODO: if _current().type == type: return _advance()
        # TODO: else: raise ParseError(f"Expected {type.name}, got {_current().type.name} on line {_current().line}")
        raise NotImplementedError

    def _match(self, *types: TokenType) -> bool:
        """Return True (without consuming) if the current token is one of `types`."""
        return self._current().type in types
