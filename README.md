# TinyLang Mini Compiler — CPSC323 Spring 2026

**Group Members**
| Role | Name |
|------|------|
| Student 1 — Lexer | Omar Rafiq 
| Student 2 — Parser | _fill in_
| Student 3 — Semantic & IR | _fill in_

---

## What This Does

Takes a small program written in TinyLang and runs it through a 4-stage compiler front-end:

```
Source Code → [Lexer] → Tokens → [Parser] → AST → [Semantic Analyzer] → [IR Generator] → Three-Address Code
```

**Example input:**
```
int x;
int y;
x = 5;
y = 3;
if (x > y) {
    x = x + y;
}
```

**Example output:**
```
t1 = x > y
if x > y goto L1
goto L2
L1:
t2 = x + y
x = t2
L2:
```

---

## How to Run

```bash
# Run on the built-in sample program
python main.py

# Run on your own file
python main.py myprogram.tl
```

**Requirements:** Python 3.10+, no external libraries needed.

---

## File Structure

```
mini-compiler/
├── token_types.py   # Token definitions (Student 1)
├── lexer.py         # Scanner — source → token list (Student 1)
├── ast_nodes.py     # AST node classes (Student 2)
├── parser.py        # Parser — tokens → AST (Student 2)
├── symbol_table.py  # Scope-aware symbol table (Student 3)
├── semantic.py      # Semantic checker (Student 3)
├── ir_gen.py        # Three-address code generator (Student 3)
├── main.py          # Runs the full pipeline
└── tests/
    ├── test_lexer.py
    ├── test_parser.py
    └── test_semantic.py
```

---

## TinyLang — Language Overview

| Feature | Syntax |
|---------|--------|
| Variable declaration | `int x;` |
| Assignment | `x = 5;` |
| Arithmetic | `x + y`, `x - y`, `x * y`, `x / y` |
| Comparison | `x < y`, `x > y`, `x == y` |
| If / else | `if (x > 0) { ... } else { ... }` |
| While loop | `while (x > 0) { ... }` |
| Block scope | `{ ... }` — variables declared inside stay inside |

---

## Running the Tests

```bash
python tests/test_lexer.py      # Student 1
python tests/test_parser.py     # Student 2
python tests/test_semantic.py   # Student 3
```

