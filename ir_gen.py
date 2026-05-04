"""
STUDENT 3 — Intermediate Representation Generator (Three-Address Code)
"""

from ast_nodes import (
    ASTNode, ProgramNode, VarDeclNode, AssignNode, BlockNode,
    IfNode, WhileNode, BinaryOpNode, NumberNode, IdentifierNode,
)


class IRGenerator:
    def __init__(self):
        self.instructions: list[str] = []
        self._temp_count = 0
        self._label_count = 0

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate(self, tree: ProgramNode) -> list[str]:
        self._visit(tree)
        return self.instructions

    def print_ir(self) -> None:
        for instr in self.instructions:
            print(instr)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _new_temp(self) -> str:
        self._temp_count += 1
        return f"t{self._temp_count}"

    def _new_label(self) -> str:
        self._label_count += 1
        return f"L{self._label_count}"

    def _emit(self, instruction: str) -> None:
        self.instructions.append(instruction)

    # ------------------------------------------------------------------
    # Dispatcher
    # ------------------------------------------------------------------

    def _visit(self, node: ASTNode) -> str:
        method = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method)
        return visitor(node)

    # ------------------------------------------------------------------
    # Visitors
    # ------------------------------------------------------------------

    def _visit_ProgramNode(self, node: ProgramNode) -> str:
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_VarDeclNode(self, node: VarDeclNode) -> str:
        return ""

    def _visit_AssignNode(self, node: AssignNode) -> str:
        result = self._visit(node.value)
        self._emit(f"{node.var_name} = {result}")

    def _visit_BlockNode(self, node: BlockNode) -> str:
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_IfNode(self, node: IfNode) -> str:
        l_then = self._new_label()
        l_end = self._new_label()

        lhs = self._visit(node.condition.left)
        rhs = self._visit(node.condition.right)

        self._emit(f"if {lhs} {node.condition.op} {rhs} goto {l_then}")
        self._emit(f"goto {l_end}")

        # THEN
        self._emit(f"{l_then}:")
        self._visit(node.then_block)

        if node.else_block:
            l_else = self._new_label()
            self._emit(f"goto {l_else}")
            self._emit(f"{l_end}:")
            self._visit(node.else_block)
            self._emit(f"{l_else}:")
        else:
            self._emit(f"{l_end}:")

    def _visit_WhileNode(self, node: WhileNode) -> str:
        l_start = self._new_label()
        l_body = self._new_label()
        l_end = self._new_label()

        self._emit(f"{l_start}:")

        lhs = self._visit(node.condition.left)
        rhs = self._visit(node.condition.right)

        self._emit(f"if {lhs} {node.condition.op} {rhs} goto {l_body}")
        self._emit(f"goto {l_end}")

        self._emit(f"{l_body}:")
        self._visit(node.body)
        self._emit(f"goto {l_start}")

        self._emit(f"{l_end}:")

    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> str:
        left = self._visit(node.left)
        right = self._visit(node.right)

        temp = self._new_temp()
        self._emit(f"{temp} = {left} {node.op} {right}")

        return temp

    def _visit_NumberNode(self, node: NumberNode) -> str:
        return str(node.value)

    def _visit_IdentifierNode(self, node: IdentifierNode) -> str:
        return node.name