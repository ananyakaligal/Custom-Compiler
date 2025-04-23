import re
from layer_ast import (
    Program, VarDecl, Assignment,
    WriteStmt, LoopFor, LoopWhile,
    IfStmt, Block, Expr
)
from symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self, tree: Program):
        self.tree = tree
        self.symbols = SymbolTable()  # global scope

    def analyze(self):
        self._visit_block(self.tree.statements, self.symbols)

    def get_symbols(self):
        return self.symbols  # for Streamlit GUI

    def _visit_block(self, stmts, table):
        for stmt in stmts:
            self._visit_stmt(stmt, table)

    def _visit_stmt(self, stmt, table):
        # Variable declaration (cvar or ivar)
        if isinstance(stmt, VarDecl):
            initialized = stmt.expr is not None
            if stmt.kind == 'ivar' and not initialized:
                raise Exception(f"ivar '{stmt.name}' must be initialized")
            value = stmt.expr.value if stmt.expr else None
            table.define(stmt.name, stmt.kind, initialized, value)

        # Assignment
        elif isinstance(stmt, Assignment):
            sym = table.lookup(stmt.name)
            if not sym:
                raise Exception(f"Undeclared identifier '{stmt.name}' in assignment")
            self._check_expr(stmt.expr, table)
            sym.initialized = True
            sym.value = stmt.expr.value

        # Write/FWrite
        elif isinstance(stmt, WriteStmt):
            for expr in stmt.args:
                self._check_expr(expr, table)

        # For-loop (creates new scope)
        elif isinstance(stmt, LoopFor):
            inner = table.enter_scope()
            inner.define(stmt.var, 'ivar', initialized=True, value=0)
            self._check_expr(stmt.count, table)
            self._visit_block(stmt.block.statements, inner)

        # While-loop (same scope)
        elif isinstance(stmt, LoopWhile):
            self._check_expr(stmt.condition, table)
            self._visit_block(stmt.block.statements, table)

        # If-statement (same scope)
        elif isinstance(stmt, IfStmt):
            self._check_expr(stmt.condition, table)
            self._visit_block(stmt.block.statements, table)

        else:
            raise Exception(f"Unknown AST node in semantic analyzer: {stmt}")

    def _check_expr(self, expr: Expr, table):
        # Remove string literals
        cleaned = re.sub(r'"[^"]*"', '', expr.value)

        for token in cleaned.split():
            if token.isdigit() or token.replace('.', '', 1).isdigit():
                continue  # numeric
            if token in ('true', 'false'):
                continue  # boolean
            if token in {'+', '-', '*', '/', '%', '^',
                         '==', '!=', '<', '>', '<=', '>=',
                         'and', 'or', 'not'}:
                continue  # operator
            sym = table.lookup(token)
            if not sym:
                raise Exception(f"Undeclared identifier '{token}' in expression '{expr.value}'")
