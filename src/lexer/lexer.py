# lexer.py
import re

token_specs = [
    ("COMMENT", r"#.*"),
    ("INDENT", r"^ {4}"),
    ("NEWLINE", r"\n"),
    ("WHITESPACE", r"[ \t]+"),
    ("ARROW", r"->"),
    ("KEYWORD", r"cvar|ivar|if|else|while|for|break|continue|def|return|class|import|from|as|loop|times|write|fwrite"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r'".*?"'),
    ("OPERATOR", r"\+|-|\*|/|%|\^|=|==|!=|<|>|<=|>=|and|or|not"),
    ("PUNCTUATION", r"[.,:()\[\]{}]"),
    ("BOOLEAN", r"true|false"),
]

token_regex = "|".join(f"(?P<{name}>{regex})" for name, regex in token_specs)

def tokenize(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "WHITESPACE":
            continue  # Ignore whitespace
        tokens.append((kind, value))
    return tokens

if __name__ == "__main__":
    with open("input.layer", "r") as f:
        code = f.read()
    tokens = tokenize(code)
    for token in tokens:
        print(token)