"""
STUDENT 3 — Semantic Analyzer

Responsibilities:
  - Walk the AST (visitor pattern)
  - Use SymbolTable to enforce:
      * No undeclared variable use
      * No duplicate declarations in the same scope
      * Basic type compatibility (e.g., no mixing types in expressions)
  - Annotate each IdentifierNode with its resolved type (optional but useful for IR)
  - Raise SemanticError on any violation

Visitor pattern: one _visit_<NodeType> method per AST node class.
Call self._visit(node) to dispatch generically.
"""

from ast_nodes import (
    ASTNode, ProgramNode, VarDeclNode, AssignNode, BlockNode,
    IfNode, WhileNode, BinaryOpNode, NumberNode, IdentifierNode,
)
from symbol_table import SymbolTable, SymbolError


class SemanticError(Exception):
    """Raised when the AST violates semantic rules."""


class SemanticAnalyzer:
    def __init__(self):
        self.table = SymbolTable()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def analyze(self, tree: ProgramNode) -> None:
        """
        Entry point. Walk the full AST and enforce all semantic rules.
        Raises SemanticError on the first violation found.
        """
        # TODO: call self._visit(tree)
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Dispatcher
    # ------------------------------------------------------------------

    def _visit(self, node: ASTNode) -> str:
        """
        Dispatch to the correct _visit_* method based on node type.
        Returns the resolved type string (e.g. 'int') so expressions
        can propagate types upward.
        """
        method = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method, self._visit_unknown)
        return visitor(node)

    def _visit_unknown(self, node: ASTNode) -> str:
        raise SemanticError(f"No visitor for node type: {type(node).__name__}")

    # ------------------------------------------------------------------
    # Visitors — one per node type
    # ------------------------------------------------------------------

    def _visit_ProgramNode(self, node: ProgramNode) -> str:
        # TODO: for stmt in node.statements: self._visit(stmt)
        raise NotImplementedError

    def _visit_VarDeclNode(self, node: VarDeclNode) -> str:
        """Declare the variable in the current scope."""
        # TODO: try self.table.declare(node.var_name, node.type_name, node.line)
        # TODO: except SymbolError as e: raise SemanticError(str(e))
        raise NotImplementedError

    def _visit_AssignNode(self, node: AssignNode) -> str:
        """
        1. Look up var_name (must be declared).
        2. Visit the value expression to get its type.
        3. Check that types match.
        """
        # TODO: try var_type = self.table.lookup_type(node.var_name, node.line)
        # TODO: except SymbolError as e: raise SemanticError(str(e))
        # TODO: val_type = self._visit(node.value)
        # TODO: if var_type != val_type: raise SemanticError(f"Type mismatch: cannot assign {val_type} to {var_type}")
        raise NotImplementedError

    def _visit_BlockNode(self, node: BlockNode) -> str:
        """Enter a new scope, visit all statements, exit scope."""
        # TODO: self.table.enter_scope()
        # TODO: for stmt in node.statements: self._visit(stmt)
        # TODO: self.table.exit_scope()
        raise NotImplementedError

    def _visit_IfNode(self, node: IfNode) -> str:
        # TODO: self._visit(node.condition)
        # TODO: self._visit(node.then_block)
        # TODO: if node.else_block: self._visit(node.else_block)
        raise NotImplementedError

    def _visit_WhileNode(self, node: WhileNode) -> str:
        # TODO: self._visit(node.condition)
        # TODO: self._visit(node.body)
        raise NotImplementedError

    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> str:
        """
        Visit both sides, check compatible types, return result type.
        For now TinyLang only has 'int', so both sides must be 'int'.
        """
        # TODO: left_type  = self._visit(node.left)
        # TODO: right_type = self._visit(node.right)
        # TODO: if left_type != right_type: raise SemanticError(f"Type mismatch in '{node.op}': {left_type} vs {right_type}")
        # TODO: return left_type   (both are the same, result is same type)
        raise NotImplementedError

    def _visit_NumberNode(self, node: NumberNode) -> str:
        return "int"

    def _visit_IdentifierNode(self, node: IdentifierNode) -> str:
        """Look up the variable and return its declared type."""
        # TODO: try return self.table.lookup_type(node.name, node.line)
        # TODO: except SymbolError as e: raise SemanticError(str(e))
        raise NotImplementedError
