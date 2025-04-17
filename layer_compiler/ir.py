# ir.py

class Instruction:
    """Base class for all IR instructions."""
    pass

class LoadConst(Instruction):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def __repr__(self):
        return f"LOAD_CONST {self.value!r} -> {self.target}"

class LoadVar(Instruction):
    def __init__(self, name, target):
        self.name = name
        self.target = target
    def __repr__(self):
        return f"LOAD_VAR {self.name} -> {self.target}"

class Add(Instruction):
    def __init__(self, left, right, target):
        self.left = left; self.right = right; self.target = target
    def __repr__(self):
        return f"ADD {self.left}, {self.right} -> {self.target}"

class Sub(Instruction):
    def __init__(self, left, right, target):
        self.left = left; self.right = right; self.target = target
    def __repr__(self):
        return f"SUB {self.left}, {self.right} -> {self.target}"

class Mul(Instruction):
    def __init__(self, left, right, target):
        self.left = left; self.right = right; self.target = target
    def __repr__(self):
        return f"MUL {self.left}, {self.right} -> {self.target}"

class Div(Instruction):
    def __init__(self, left, right, target):
        self.left = left; self.right = right; self.target = target
    def __repr__(self):
        return f"DIV {self.left}, {self.right} -> {self.target}"

class Pow(Instruction):
    def __init__(self, base, exp, target):
        self.base = base; self.exp = exp; self.target = target
    def __repr__(self):
        return f"POW {self.base}, {self.exp} -> {self.target}"

class StoreVar(Instruction):
    def __init__(self, source, name):
        self.source = source; self.name = name
    def __repr__(self):
        return f"STORE_VAR {self.source} -> {self.name}"

class CallWrite(Instruction):
    def __init__(self, arg):
        self.arg = arg
    def __repr__(self):
        return f"CALL_WRITE {self.arg}"

class PrintNewline(Instruction):
    """Emit a newline after a series of CALL_WRITE instructions."""
    def __repr__(self):
        return "PRINT_NEWLINE"

class Label(Instruction):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"LABEL {self.name}"

class Jump(Instruction):
    def __init__(self, label):
        self.label = label
    def __repr__(self):
        return f"JUMP {self.label}"

class JumpIfFalse(Instruction):
    def __init__(self, cond, label):
        self.cond  = cond
        self.label = label
    def __repr__(self):
        return f"JUMP_IF_FALSE {self.cond} -> {self.label}"

class TempGenerator:
    """Generates fresh temporary names (_t0, _t1, ...)."""
    def __init__(self):
        self.counter = 0
    def new_temp(self):
        name = f"_t{self.counter}"
        self.counter += 1
        return name

class LabelGenerator:
    """Generates fresh labels (L0, L1, ...)."""
    def __init__(self):
        self.counter = 0
    def new_label(self, base="L"):
        name = f"{base}{self.counter}"
        self.counter += 1
        return name
