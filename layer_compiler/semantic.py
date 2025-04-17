# semantic.py

import re
from ast import (
    Program, VarDecl, Assignment,
    WriteStmt, LoopFor, LoopWhile,
    IfStmt, Block, Expr
)
from symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self, tree: Program):
        self.tree    = tree
        self.globals = SymbolTable()

    def analyze(self):
        self._visit_block(self.tree.statements, self.globals)

    def _visit_block(self, stmts, table):
        for stmt in stmts:
            self._visit_stmt(stmt, table)

    def _visit_stmt(self, stmt, table):
        # var declaration
        if isinstance(stmt, VarDecl):
            initialized = stmt.expr is not None
            if stmt.kind == 'ivar' and not initialized:
                raise Exception(f"ivar '{stmt.name}' must be initialized")
            table.define(stmt.name, stmt.kind, initialized)

        # assignment
        elif isinstance(stmt, Assignment):
            sym = table.lookup(stmt.name)
            if not sym:
                raise Exception(f"Undeclared identifier '{stmt.name}' in assignment")
            self._check_expr(stmt.expr, table)
            sym.initialized = True

        # write/fwrite
        elif isinstance(stmt, WriteStmt):
            for expr in stmt.args:
                self._check_expr(expr, table)

        # for-loop
        elif isinstance(stmt, LoopFor):
            inner = table.enter_scope()
            inner.define(stmt.var, 'ivar', initialized=True)
            self._check_expr(stmt.count, table)
            self._visit_block(stmt.block.statements, inner)

        # while-loop
        elif isinstance(stmt, LoopWhile):
            self._check_expr(stmt.condition, table)
            self._visit_block(stmt.block.statements, table)

        # if-statement
        elif isinstance(stmt, IfStmt):
            self._check_expr(stmt.condition, table)
            self._visit_block(stmt.block.statements, table)

        else:
            raise Exception(f"Unknown AST node in semantic analyzer: {stmt}")

    def _check_expr(self, expr: Expr, table):
        # 1) Remove all string literals so they don't split on spaces
        #    e.g. '"Hello world"' → ''
        s = re.sub(r'"[^"]*"', '', expr.value)

        # 2) Split on whitespace and validate each remaining token
        for tok in s.split():
            # numeric literal
            if tok.isdigit() or tok.replace('.', '', 1).isdigit():
                continue
            # boolean literal
            if tok in ('true', 'false'):
                continue
            # operators
            if tok in {'+', '-', '*', '/', '%', '^',
                       '==', '!=', '<', '>', '<=', '>=',
                       'and', 'or', 'not'}:
                continue
            # else: must be a declared identifier
            sym = table.lookup(tok)
            if not sym:
                raise Exception(f"Undeclared identifier '{tok}' in expression '{expr.value}'")
