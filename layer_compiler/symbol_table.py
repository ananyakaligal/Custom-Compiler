class Symbol:
    def __init__(self, name, kind, initialized=False, value=None):
        self.name        = name            # variable name
        self.kind        = kind            # 'cvar' or 'ivar'
        self.initialized = initialized     # boolean
        self.value       = value           # optional value

    def __repr__(self):
        return f"Symbol({self.name}, {self.kind}, init={self.initialized}, value={self.value})"


class SymbolTable:
    def __init__(self, parent=None):
        self.parent  = parent
        self.symbols = {}  # maps name -> Symbol

    def define(self, name, kind, initialized=False, value=None):
        if name in self.symbols:
            raise Exception(f"Duplicate declaration of '{name}'")
        sym = Symbol(name, kind, initialized, value)
        self.symbols[name] = sym
        return sym

    def lookup(self, name):
        table = self
        while table:
            if name in table.symbols:
                return table.symbols[name]
            table = table.parent
        return None

    def enter_scope(self):
        return SymbolTable(parent=self)

    def exit_scope(self):
        return self.parent

    def as_list(self):
        """
        Convert symbol table into a list of dictionaries for DataFrame display.
        """
        entries = []
        for name, sym in self.symbols.items():
            entries.append({
                "Name": sym.name,
                "Type": sym.kind,
                "Initialized": sym.initialized,
                "Value": sym.value
            })
        return entries
