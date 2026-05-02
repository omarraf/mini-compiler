# TinyLang Mini Compiler — CPSC323 Spring 2026

**Group Members**
| Role | Name | CWID |
|------|------|------|
| Student 1 — Lexer | Omar Rafiq | _fill in_ |
| Student 2 — Parser | _fill in_ | _fill in_ |
| Student 3 — Semantic & IR | _fill in_ | _fill in_ |

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

Each student runs their own test file independently — no test framework needed.

```bash
python tests/test_lexer.py      # Student 1
python tests/test_parser.py     # Student 2
python tests/test_semantic.py   # Student 3
```

---

## Build Order

Students should complete work in this order since each stage depends on the previous:

1. **Student 1** — finish `lexer.py` first, everyone else is blocked until tokens work
2. **Student 2** — finish `parser.py` once tokens are working
3. **Student 3** — can start `symbol_table.py` and `semantic.py` immediately using hardcoded AST nodes, then wire up to the real parser when it's ready

---

## What Each Student Needs to Implement

All `raise NotImplementedError` stubs have `# TODO:` comments with the exact steps.

**Student 1 (`lexer.py`)** — 7 methods
- `tokenize()` — main scan loop
- `_current()`, `_advance()`, `_peek()` — move through source characters
- `_skip_whitespace()` — handle spaces/newlines, track line number
- `_read_number()` — collect digit characters into a NUMBER token
- `_read_identifier_or_keyword()` — collect word characters, check against keywords

**Student 2 (`parser.py`)** — 12 methods
- `parse()` — entry point, returns the AST root
- `_parse_statement()` — picks the right rule based on current token
- `_parse_var_decl()`, `_parse_assign()`, `_parse_if()`, `_parse_while()`, `_parse_block()`
- `_parse_expression()`, `_parse_comparison()`, `_parse_addition()`, `_parse_term()`, `_parse_factor()`
- `_expect()` — consume a required token or raise ParseError

**Student 3 (`symbol_table.py` + `semantic.py` + `ir_gen.py`)** — 19 methods
- Symbol table: `enter_scope()`, `exit_scope()`, `declare()`, `lookup()`
- Semantic: one `_visit_*` method per AST node type
- IR: one `_visit_*` method per AST node type, using `_new_temp()` and `_new_label()`
