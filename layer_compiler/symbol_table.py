# symbol_table.py

class Symbol:
    def __init__(self, name, kind, initialized=False):
        self.name        = name       # variable name
        self.kind        = kind       # 'cvar' or 'ivar'
        self.initialized = initialized

    def __repr__(self):
        return f"Symbol({self.name}, {self.kind}, init={self.initialized})"

class SymbolTable:
    def __init__(self, parent=None):
        self.parent  = parent
        self.symbols = {}    # maps name -> Symbol

    def define(self, name, kind, initialized=False):
        if name in self.symbols:
            raise Exception(f"Duplicate declaration of '{name}'")
        sym = Symbol(name, kind, initialized)
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
