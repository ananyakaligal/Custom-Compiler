# token_defs.py

class Token:
    def __init__(self, type_, value, line, column):
        self.type  = type_
        self.value = value
        self.line  = line
        self.col   = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.col})"
