"""
STUDENT 3 — Semantic Analyzer
"""

from ast_nodes import (
    ASTNode, ProgramNode, VarDeclNode, AssignNode, BlockNode,
    IfNode, WhileNode, BinaryOpNode, NumberNode, IdentifierNode,
)
from symbol_table import SymbolTable, SymbolError


class SemanticError(Exception):
    """Raised when the AST violates semantic rules."""
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.table = SymbolTable()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def analyze(self, tree: ProgramNode) -> None:
        """Start semantic analysis"""
        self._visit(tree)

    # ------------------------------------------------------------------
    # Dispatcher
    # ------------------------------------------------------------------

    def _visit(self, node: ASTNode) -> str:
        method = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method, self._visit_unknown)
        return visitor(node)

    def _visit_unknown(self, node: ASTNode) -> str:
        raise SemanticError(f"No visitor for node type: {type(node).__name__}")

    # ------------------------------------------------------------------
    # Visitors
    # ------------------------------------------------------------------

    def _visit_ProgramNode(self, node: ProgramNode) -> str:
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_VarDeclNode(self, node: VarDeclNode) -> str:
        try:
            self.table.declare(node.var_name, node.type_name, node.line)
        except SymbolError as e:
            raise SemanticError(str(e))

    def _visit_AssignNode(self, node: AssignNode) -> str:
        try:
            var_type = self.table.lookup_type(node.var_name, node.line)
        except SymbolError as e:
            raise SemanticError(str(e))

        val_type = self._visit(node.value)

        if var_type != val_type:
            raise SemanticError(
                f"Type mismatch: cannot assign {val_type} to {var_type}"
            )

    def _visit_BlockNode(self, node: BlockNode) -> str:
        self.table.enter_scope()

        for stmt in node.statements:
            self._visit(stmt)

        self.table.exit_scope()

    def _visit_IfNode(self, node: IfNode) -> str:
        self._visit(node.condition)
        self._visit(node.then_block)

        if node.else_block:
            self._visit(node.else_block)

    def _visit_WhileNode(self, node: WhileNode) -> str:
        self._visit(node.condition)
        self._visit(node.body)

    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> str:
        left_type = self._visit(node.left)
        right_type = self._visit(node.right)

        if left_type != right_type:
            raise SemanticError(
                f"Type mismatch in '{node.op}': {left_type} vs {right_type}"
            )

        return left_type

    def _visit_NumberNode(self, node: NumberNode) -> str:
        return "int"

    def _visit_IdentifierNode(self, node: IdentifierNode) -> str:
        try:
            return self.table.lookup_type(node.name, node.line)
        except SymbolError as e:
            raise SemanticError(str(e))