# parser.py

from lexer import Lexer
from token_defs import Token
from ast import (
    Program, VarDecl, WriteStmt,
    LoopFor, LoopWhile, IfStmt,
    Block, Expr
)

class Parser:
    def __init__(self, source: str):
        self.tokens = Lexer(source).tokenize()
        self.pos    = 0
        self.cur    = self.tokens[0]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.cur = self.tokens[self.pos]

    def eat(self, ttype, value=None):
        if self.cur.type != ttype or (value is not None and self.cur.value != value):
            raise SyntaxError(f"Expected {ttype} {value}, got {self.cur}")
        self.advance()

    def parse(self):
        stmts = []
        while self.cur.type != 'EOF':
            if self.cur.type == 'NEWLINE':
                self.advance()
                continue
            stmts.append(self.parse_stmt())
        return Program(stmts)

    def parse_stmt(self):
        # 1) Variable declaration: cvar or ivar
        if self.cur.type == 'KEYWORD' and self.cur.value in ('cvar', 'ivar'):
            kind = self.cur.value
            self.advance()
            name = self.cur.value
            self.eat('IDENTIFIER')
            expr = None
            if self.cur.type == 'OPERATOR' and self.cur.value == '=':
                self.advance()
                expr = self.parse_expr()
            if self.cur.type == 'NEWLINE':
                self.advance()
            return VarDecl(kind, name, expr)

        # 2) write / fwrite
        if self.cur.type == 'IDENTIFIER' and self.cur.value in ('write', 'fwrite'):
            is_f = (self.cur.value == 'fwrite')
            self.advance()
            self.eat('PUNCTUATION', '(')
            args = self.parse_args()
            self.eat('PUNCTUATION', ')')
            if self.cur.type == 'NEWLINE':
                self.advance()
            return WriteStmt(args, is_fwrite=is_f)

        # 3) loop (for / while)
        if self.cur.type == 'IDENTIFIER' and self.cur.value == 'loop':
            self.advance()
            # while
            if self.cur.type == 'KEYWORD' and self.cur.value == 'while':
                self.advance()
                cond = self.parse_expr()
                self.eat('OPERATOR', '->')
                blk = self.parse_block()
                return LoopWhile(cond, blk)
            # for
            var = self.cur.value
            self.eat('IDENTIFIER')
            self.eat('KEYWORD', 'for')
            count = self.parse_expr()
            # skip optional 'times'
            if self.cur.type == 'IDENTIFIER' and self.cur.value == 'times':
                self.advance()
            # strip 'times' if in expr value
            if isinstance(count, Expr) and count.value.endswith(' times'):
                count = Expr(count.value[:-6].strip())
            self.eat('OPERATOR', '->')
            blk = self.parse_block()
            return LoopFor(var, count, blk)

        # 4) if statement
        if self.cur.type == 'KEYWORD' and self.cur.value == 'if':
            self.advance()
            cond = self.parse_expr()
            self.eat('OPERATOR', '->')
            blk = self.parse_block()
            return IfStmt(cond, blk)

        raise SyntaxError(f"Unknown statement at {self.cur}")

    def parse_args(self):
        args = []
        while True:
            args.append(self.parse_expr())
            if self.cur.type == 'PUNCTUATION' and self.cur.value == ',':
                self.advance()
                continue
            break
        return args

    def parse_expr(self):
        # collect tokens until we hit a delimiter (newline, EOF, comma, closing paren/brace, or arrow)
        tokens = []
        stop_types = ('NEWLINE', 'EOF')
        stop_punc = (',', ')', '{', '}')
        while self.cur.type not in stop_types \
          and not (self.cur.type == 'PUNCTUATION' and self.cur.value in stop_punc) \
          and not (self.cur.type == 'OPERATOR' and self.cur.value == '->'):
            tokens.append(self.cur.value)
            self.advance()
        return Expr(' '.join(tokens))

    def parse_block(self):
        # 1) Single-statement block (no braces)
        if not (self.cur.type == 'PUNCTUATION' and self.cur.value == '{'):
            stmt = self.parse_stmt()
            return Block([stmt])

        # 2) Braced block
        self.eat('PUNCTUATION', '{')
        stmts = []
        while not (self.cur.type == 'PUNCTUATION' and self.cur.value == '}'):
            # skip indentation and blank lines inside braces
            if self.cur.type in ('NEWLINE', 'INDENT'):
                self.advance()
                continue
            stmts.append(self.parse_stmt())
        self.eat('PUNCTUATION', '}')
        # consume trailing newline if present
        if self.cur.type == 'NEWLINE':
            self.advance()
        return Block(stmts)
