"""
Pipeline runner — ties all components together.
Run:  python main.py <source_file.tl>
      python main.py  (uses built-in sample if no file given)
"""

import sys

from lexer import Lexer, LexerError
from parser import Parser, ParseError
from semantic import SemanticAnalyzer, SemanticError
from ir_gen import IRGenerator


SAMPLE_PROGRAM = """\
int x;
int y;
int z;
x = 5;
y = 3;
if (x > y) {
    z = x + y;
}
while (z > 0) {
    z = z - 1;
}
"""


def run(source: str) -> None:
    print("=" * 40)
    print("SOURCE")
    print("=" * 40)
    print(source)

    # ── Stage 1: Lexer ──────────────────────────────────────────────
    print("=" * 40)
    print("TOKENS")
    print("=" * 40)
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        for tok in tokens:
            print(tok)
    except LexerError as e:
        print(f"[Lexer Error] {e}")
        return

    # ── Stage 2: Parser ─────────────────────────────────────────────
    print("=" * 40)
    print("AST")
    print("=" * 40)
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        # TODO (Student 2): add a pretty-printer for the AST
        print(ast)
    except ParseError as e:
        print(f"[Parse Error] {e}")
        return

    # ── Stage 3: Semantic Analysis ──────────────────────────────────
    print("=" * 40)
    print("SEMANTIC CHECK")
    print("=" * 40)
    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("OK — no semantic errors")
    except SemanticError as e:
        print(f"[Semantic Error] {e}")
        return

    # ── Stage 4: IR Generation ──────────────────────────────────────
    print("=" * 40)
    print("THREE-ADDRESS CODE")
    print("=" * 40)
    gen = IRGenerator()
    gen.generate(ast)
    gen.print_ir()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            source = f.read()
    else:
        source = SAMPLE_PROGRAM

    run(source)
