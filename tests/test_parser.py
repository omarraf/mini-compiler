"""STUDENT 2 — Parser tests."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lexer import Lexer
from parser import Parser, ParseError
from ast_nodes import ProgramNode, VarDeclNode, AssignNode, IfNode, WhileNode


def _parse(source: str) -> ProgramNode:
    return Parser(Lexer(source).tokenize()).parse()


def test_var_decl():
    tree = _parse("int x;")
    assert len(tree.statements) == 1
    node = tree.statements[0]
    assert isinstance(node, VarDeclNode)
    assert node.var_name == "x"
    assert node.type_name == "int"


def test_assign():
    tree = _parse("int x; x = 5;")
    assign = tree.statements[1]
    assert isinstance(assign, AssignNode)
    assert assign.var_name == "x"


def test_if_no_else():
    tree = _parse("if (1 < 2) { int x; }")
    assert isinstance(tree.statements[0], IfNode)
    assert tree.statements[0].else_block is None


def test_if_else():
    tree = _parse("if (1 < 2) { int x; } else { int y; }")
    node = tree.statements[0]
    assert isinstance(node, IfNode)
    assert node.else_block is not None


def test_while():
    tree = _parse("while (1 < 2) { int x; }")
    assert isinstance(tree.statements[0], WhileNode)


def test_syntax_error():
    try:
        _parse("int ;")   # missing identifier
        assert False, "Expected ParseError"
    except ParseError:
        pass


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"  PASS  {name}")
            except Exception as e:
                print(f"  FAIL  {name}: {e}")
