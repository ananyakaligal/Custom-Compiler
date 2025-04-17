# rules.py

# Order matters: longer patterns first
TOKEN_REGEX = [
    ('COMMENT',     r'#.*'),                                      # whole-line comment
    ('NEWLINE',     r'\n'),
    ('INDENT',      r' {4}'),                                     # exactly 4 spaces
    ('WHITESPACE',  r'[ \t]+'),
    ('KEYWORD',     r'\b(?:cvar|ivar|if|else|while|for|break|continue|def|return|class|import|from|as)\b'),
    ('BOOLEAN',     r'\b(?:true|false)\b'),
    ('IDENTIFIER',  r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('NUMBER',      r'\b[0-9]+(?:\.[0-9]+)?\b'),
    ('STRING',      r'"[^"\n]*"'),
    ('OPERATOR',    r'->|==|!=|<=|>=|and|or|not|\+|-|\*|/|%|\^|=|<|>'),
    ('PUNCTUATION', r'[.,:()\[\]{}]'),
]
