"""
STUDENT 3 — Intermediate Representation Generator (Three-Address Code)

Responsibilities:
  - Walk the semantically-checked AST
  - Emit TAC instructions (strings) into self.instructions
  - Manage temporary variables (t1, t2, ...) and labels (L1, L2, ...)
  - Print or return the final instruction list

Three-Address Code format:
  Assignments:    t1 = y * 2
  Conditionals:   if x < y goto L1 / goto L2
  Labels:         L1:
  Copy:           x = t1

Example for  if (x < y) { z = x + 1; }:
  if x < y goto L1
  goto L2
  L1:
      t1 = x + 1
      z = t1
  L2:
"""

from ast_nodes import (
    ASTNode, ProgramNode, VarDeclNode, AssignNode, BlockNode,
    IfNode, WhileNode, BinaryOpNode, NumberNode, IdentifierNode,
)


class IRGenerator:
    def __init__(self):
        self.instructions: list[str] = []
        self._temp_count = 0    # increment to get unique temp names
        self._label_count = 0   # increment to get unique label names

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate(self, tree: ProgramNode) -> list[str]:
        """
        Entry point. Walk the AST and populate self.instructions.
        Return the completed instruction list.
        """
        # TODO: self._visit(tree)
        # TODO: return self.instructions
        raise NotImplementedError

    def print_ir(self) -> None:
        """Print each instruction on its own line (for demo output)."""
        for instr in self.instructions:
            print(instr)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _new_temp(self) -> str:
        """Return the next unique temporary name: t1, t2, ..."""
        self._temp_count += 1
        return f"t{self._temp_count}"

    def _new_label(self) -> str:
        """Return the next unique label name: L1, L2, ..."""
        self._label_count += 1
        return f"L{self._label_count}"

    def _emit(self, instruction: str) -> None:
        """Append one TAC instruction to the list."""
        self.instructions.append(instruction)

    # ------------------------------------------------------------------
    # Visitors — one per node type
    # ------------------------------------------------------------------

    def _visit(self, node: ASTNode) -> str:
        """
        Dispatch to _visit_<NodeType>.
        For expression nodes, returns the name holding the result (temp or literal).
        For statement nodes, return value is ignored.
        """
        method = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method)
        return visitor(node)

    def _visit_ProgramNode(self, node: ProgramNode) -> str:
        # TODO: for stmt in node.statements: self._visit(stmt)
        raise NotImplementedError

    def _visit_VarDeclNode(self, node: VarDeclNode) -> str:
        """Variable declarations need no TAC; they're already in the symbol table."""
        return ""

    def _visit_AssignNode(self, node: AssignNode) -> str:
        """
        1. Visit node.value → get result name (temp or literal)
        2. Emit:  var_name = result
        """
        # TODO: result = self._visit(node.value)
        # TODO: self._emit(f"{node.var_name} = {result}")
        raise NotImplementedError

    def _visit_BlockNode(self, node: BlockNode) -> str:
        # TODO: for stmt in node.statements: self._visit(stmt)
        raise NotImplementedError

    def _visit_IfNode(self, node: IfNode) -> str:
        """
        Pattern:
          if <cond_lhs> <op> <cond_rhs> goto L_then
          goto L_end
          L_then:
            <then instructions>
          [L_else:
            <else instructions>]
          L_end:
        """
        # TODO: the condition must be a BinaryOpNode with a relational op (<, >, ==)
        #       pull node.condition.left, node.condition.op, node.condition.right directly
        #       visit each side to get their result names, then emit the conditional jump
        # TODO: l_then = self._new_label()
        # TODO: l_end  = self._new_label()
        # TODO: lhs = self._visit(node.condition.left)
        # TODO: rhs = self._visit(node.condition.right)
        # TODO: self._emit(f"if {lhs} {node.condition.op} {rhs} goto {l_then}")
        # TODO: self._emit(f"goto {l_end}")
        # TODO: self._emit(f"{l_then}:")
        # TODO: self._visit(node.then_block)
        # TODO: if node.else_block:
        #           l_else = self._new_label()  (allocate before emitting l_end)
        #           emit goto l_else after then block, emit l_else:, visit else_block
        # TODO: self._emit(f"{l_end}:")
        raise NotImplementedError

    def _visit_WhileNode(self, node: WhileNode) -> str:
        """
        Pattern:
          L_start:
          if <cond_lhs> <op> <cond_rhs> goto L_body
          goto L_end
          L_body:
            <body instructions>
          goto L_start
          L_end:
        """
        # TODO: l_start = self._new_label()
        # TODO: l_body  = self._new_label()
        # TODO: l_end   = self._new_label()
        # TODO: self._emit(f"{l_start}:")
        # TODO: lhs = self._visit(node.condition.left)
        # TODO: rhs = self._visit(node.condition.right)
        # TODO: self._emit(f"if {lhs} {node.condition.op} {rhs} goto {l_body}")
        # TODO: self._emit(f"goto {l_end}")
        # TODO: self._emit(f"{l_body}:")
        # TODO: self._visit(node.body)
        # TODO: self._emit(f"goto {l_start}")
        # TODO: self._emit(f"{l_end}:")
        raise NotImplementedError

    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> str:
        """
        1. Recursively get result names for left and right
        2. Allocate a new temp
        3. Emit:  temp = left op right
        4. Return temp
        """
        # TODO: left  = self._visit(node.left)
        # TODO: right = self._visit(node.right)
        # TODO: temp  = self._new_temp()
        # TODO: self._emit(f"{temp} = {left} {node.op} {right}")
        # TODO: return temp
        raise NotImplementedError

    def _visit_NumberNode(self, node: NumberNode) -> str:
        """Return the literal value as a string (no instruction needed)."""
        return str(node.value)

    def _visit_IdentifierNode(self, node: IdentifierNode) -> str:
        """Return the variable name directly."""
        return node.name
