"""
STUDENT 2 — AST Node Definitions

Each class represents one kind of node in the Abstract Syntax Tree.
Keep nodes as plain data containers (no logic here).
The parser constructs them; semantic analysis and IR generation read them.

Naming convention: every node ends in 'Node'.
"""

from dataclasses import dataclass, field
from typing import Optional


# ------------------------------------------------------------------
# Base
# ------------------------------------------------------------------

class ASTNode:
    """Base class for all AST nodes."""


# ------------------------------------------------------------------
# Statements
# ------------------------------------------------------------------

@dataclass
class ProgramNode(ASTNode):
    """Root of the tree — the entire program."""
    statements: list[ASTNode] = field(default_factory=list)


@dataclass
class VarDeclNode(ASTNode):
    """int x;  →  type_name='int', var_name='x'"""
    type_name: str
    var_name: str
    line: int = 0


@dataclass
class AssignNode(ASTNode):
    """x = <expr>;"""
    var_name: str
    value: ASTNode        # any expression node
    line: int = 0


@dataclass
class BlockNode(ASTNode):
    """{ stmt1; stmt2; ... }"""
    statements: list[ASTNode] = field(default_factory=list)


@dataclass
class IfNode(ASTNode):
    """if (<condition>) <then_block> [else <else_block>]"""
    condition: ASTNode
    then_block: BlockNode
    else_block: Optional[BlockNode] = None


@dataclass
class WhileNode(ASTNode):
    """while (<condition>) <body>"""
    condition: ASTNode
    body: BlockNode


# ------------------------------------------------------------------
# Expressions
# ------------------------------------------------------------------

@dataclass
class BinaryOpNode(ASTNode):
    """
    <left> <op> <right>
    op is the operator string: '+', '-', '*', '/', '<', '>', '=='
    """
    op: str
    left: ASTNode
    right: ASTNode


@dataclass
class NumberNode(ASTNode):
    """A literal integer."""
    value: int


@dataclass
class IdentifierNode(ASTNode):
    """A variable reference."""
    name: str
    line: int = 0
