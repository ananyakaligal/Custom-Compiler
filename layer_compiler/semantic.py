# semantic.py

from ast import (
    Program, VarDecl, WriteStmt,
    LoopFor, LoopWhile, IfStmt,
    Block, Expr
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
        if isinstance(stmt, VarDecl):
            initialized = stmt.expr is not None
            if stmt.kind == 'ivar' and not initialized:
                raise Exception(f"ivar '{stmt.name}' must be initialized")
            table.define(stmt.name, stmt.kind, initialized)

        elif isinstance(stmt, WriteStmt):
            for expr in stmt.args:
                self._check_expr(expr, table)

        elif isinstance(stmt, LoopFor):
            inner = table.enter_scope()
            inner.define(stmt.var, 'ivar', initialized=True)
            self._check_expr(stmt.count, table)
            self._visit_block(stmt.block.statements, inner)

        elif isinstance(stmt, LoopWhile):
            self._check_expr(stmt.condition, table)
            self._visit_block(stmt.block.statements, table)

        elif isinstance(stmt, IfStmt):
            self._check_expr(stmt.condition, table)
            self._visit_block(stmt.block.statements, table)

        else:
            raise Exception(f"Unknown AST node in semantic analyzer: {stmt}")

    def _check_expr(self, expr: Expr, table):
        for tok in expr.value.split():
            # numeric literal
            if tok.isdigit() or tok.replace('.', '', 1).isdigit():
                continue
            # string literal
            if tok.startswith('"') and tok.endswith('"'):
                continue
            # operators
            if tok in {'+', '-', '*', '/', '%', '^',
                       '==','!=','<','>','<=','>=',
                       'and','or','not'}:
                continue
            # must be declared
            sym = table.lookup(tok)
            if not sym:
                raise Exception(f"Undeclared identifier '{tok}' in expression '{expr.value}'")
