"""
STUDENT 3 — Symbol Table with Scope Support
"""

class SymbolError(Exception):
    """Raised on undeclared variable use or duplicate declaration."""
    pass


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
        self.scopes: list[dict[str, Symbol]] = [{}]   # global scope

    # ------------------------------------------------------------------
    # Scope management
    # ------------------------------------------------------------------

    def enter_scope(self) -> None:
        """Push a new (empty) scope onto the stack."""
        self.scopes.append({})

    def exit_scope(self) -> None:
        """Pop the innermost scope."""
        if len(self.scopes) <= 1:
            raise SymbolError("Cannot exit global scope")

        self.scopes.pop()

    # ------------------------------------------------------------------
    # Declaration & lookup
    # ------------------------------------------------------------------

    def declare(self, name: str, type_name: str, line: int = 0) -> None:
        """
        Add `name` to the current (innermost) scope.
        Raise SymbolError if duplicate in same scope.
        """
        current_scope = self.scopes[-1]

        if name in current_scope:
            raise SymbolError(f"'{name}' already declared (line {line})")

        current_scope[name] = Symbol(name, type_name)

    def lookup(self, name: str, line: int = 0) -> Symbol:
        """
        Search from innermost scope outward.
        Raise SymbolError if not found.
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]

        raise SymbolError(f"Undeclared variable '{name}' (line {line})")

    def lookup_type(self, name: str, line: int = 0) -> str:
        """Return just the type string."""
        return self.lookup(name, line).type_name