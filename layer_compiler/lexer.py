# lexer.py

import re
from token_defs import Token
from rules import TOKEN_REGEX

class Lexer:
    def __init__(self, source: str):
        self.source       = source
        self.pos          = 0
        self.line         = 1
        self.col          = 0
        self.tokens       = []
        self.indent_stack = [0]

    def tokenize(self):
        while self.pos < len(self.source):
            match = None
            for tok_type, pattern in TOKEN_REGEX:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if not match:
                    continue
                text = match.group(0)
                self.pos += len(text)

                if tok_type == 'WHITESPACE':
                    self.col += len(text)
                elif tok_type == 'COMMENT':
                    # skip comment
                    pass
                elif tok_type == 'NEWLINE':
                    self.tokens.append(Token('NEWLINE', '\\n', self.line, self.col))
                    self.line += 1
                    self.col   = 0
                elif tok_type == 'INDENT':
                    self.tokens.append(Token('INDENT', text, self.line, self.col))
                    self.col += len(text)
                else:
                    self.tokens.append(Token(tok_type, text, self.line, self.col))
                    self.col += len(text)
                break

            if not match:
                raise SyntaxError(
                    f"Unexpected character {self.source[self.pos]!r} at "
                    f"line {self.line}, col {self.col}"
                )

        self.tokens.append(Token('EOF', '', self.line, self.col))
        return self.tokens
