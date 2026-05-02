"""STUDENT 3 — Semantic analysis and IR tests."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer, SemanticError
from ir_gen import IRGenerator


def _analyze(source: str):
    tree = Parser(Lexer(source).tokenize()).parse()
    SemanticAnalyzer().analyze(tree)
    return tree


def _ir(source: str) -> list[str]:
    tree = _analyze(source)
    gen = IRGenerator()
    gen.generate(tree)
    return gen.instructions


# ── Semantic tests ────────────────────────────────────────────────────

def test_undeclared_variable():
    try:
        _analyze("x = 5;")   # x never declared
        assert False, "Expected SemanticError"
    except SemanticError:
        pass


def test_duplicate_declaration():
    try:
        _analyze("int x; int x;")
        assert False, "Expected SemanticError"
    except SemanticError:
        pass


def test_valid_program():
    _analyze("int x; x = 10;")   # should not raise


def test_nested_scope_shadow():
    # x in inner scope is a different declaration from outer x — should not raise
    _analyze("int x; { int x; x = 1; } x = 2;")


def test_undeclared_in_expression():
    try:
        _analyze("int x; x = y + 1;")   # y undeclared
        assert False, "Expected SemanticError"
    except SemanticError:
        pass


# ── IR tests ──────────────────────────────────────────────────────────

def test_ir_assign():
    instrs = _ir("int x; x = 3 + 4;")
    # should contain something like "t1 = 3 + 4" and "x = t1"
    combined = " ".join(instrs)
    assert "x" in combined
    assert "+" in combined


def test_ir_if_has_goto():
    instrs = _ir("int x; int y; x = 1; y = 2; if (x < y) { x = 0; }")
    combined = " ".join(instrs)
    assert "goto" in combined


def test_ir_while_has_loop_label():
    instrs = _ir("int x; x = 3; while (x > 0) { x = x - 1; }")
    combined = " ".join(instrs)
    assert "goto" in combined


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"  PASS  {name}")
            except Exception as e:
                print(f"  FAIL  {name}: {e}")
