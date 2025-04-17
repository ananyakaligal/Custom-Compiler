# ast.py

class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"

class VarDecl(Node):
    def __init__(self, kind, name, expr):
        self.kind = kind      # 'cvar' or 'ivar'
        self.name = name
        self.expr = expr      # may be None for cvar
    def __repr__(self):
        return f"VarDecl({self.kind}, {self.name}, {self.expr})"

class WriteStmt(Node):
    def __init__(self, args, is_fwrite=False):
        self.args = args
        self.is_fwrite = is_fwrite
    def __repr__(self):
        tag = "FWrite" if self.is_fwrite else "Write"
        return f"{tag}({self.args})"

class LoopFor(Node):
    def __init__(self, var, count, block):
        self.var = var
        self.count = count
        self.block = block
    def __repr__(self):
        return f"LoopFor({self.var}, {self.count}, {self.block})"

class LoopWhile(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
    def __repr__(self):
        return f"LoopWhile({self.condition}, {self.block})"

class IfStmt(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
    def __repr__(self):
        return f"If({self.condition}, {self.block})"

class Block(Node):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Block({self.statements})"

class Expr(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Expr({self.value})"
