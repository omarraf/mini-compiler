"""
STUDENT 3 — Symbol Table with Scope Support

Responsibilities:
  - Track every declared variable (name + type)
  - Support nested scopes: entering a block pushes a new scope,
    leaving it pops back to the enclosing one
  - Raise SymbolError on duplicate declarations or undeclared use
"""


class SymbolError(Exception):
    """Raised on undeclared variable use or duplicate declaration."""


class Symbol:
    """One entry in the symbol table."""

    def __init__(self, name: str, type_name: str):
        self.name = name
        self.type_name = type_name   # e.g. 'int'

    def __repr__(self) -> str:
        return f"Symbol({self.name}: {self.type_name})"


class SymbolTable:
    """
    A stack of scopes. Each scope is a dict mapping name → Symbol.
    Index 0 is the global (outermost) scope; the last element is innermost.
    """

    def __init__(self):
        self.scopes: list[dict[str, Symbol]] = [{}]   # start with global scope

    # ------------------------------------------------------------------
    # Scope management
    # ------------------------------------------------------------------

    def enter_scope(self) -> None:
        """Push a new (empty) scope onto the stack. Call when entering { }."""
        # TODO: append an empty dict to self.scopes
        raise NotImplementedError

    def exit_scope(self) -> None:
        """Pop the innermost scope. Call when leaving { }."""
        # TODO: self.scopes.pop()
        # TODO: guard against popping the global scope (len > 1)
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Declaration & lookup
    # ------------------------------------------------------------------

    def declare(self, name: str, type_name: str, line: int = 0) -> None:
        """
        Add `name` to the current (innermost) scope.
        Raise SymbolError if `name` is already declared in this same scope.
        """
        # TODO: current_scope = self.scopes[-1]
        # TODO: if name in current_scope: raise SymbolError(f"'{name}' already declared (line {line})")
        # TODO: current_scope[name] = Symbol(name, type_name)
        raise NotImplementedError

    def lookup(self, name: str, line: int = 0) -> Symbol:
        """
        Search from innermost scope outward.
        Return the Symbol if found.
        Raise SymbolError if `name` is not declared in any enclosing scope.
        """
        # TODO: iterate self.scopes in reverse (reversed(self.scopes))
        # TODO:   if name in scope: return scope[name]
        # TODO: raise SymbolError(f"Undeclared variable '{name}' (line {line})")
        raise NotImplementedError

    def lookup_type(self, name: str, line: int = 0) -> str:
        """Convenience wrapper: return just the type string for `name`."""
        return self.lookup(name, line).type_name
