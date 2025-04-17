# interpreter.py

from ast import (
    Program, VarDecl, Assignment,
    WriteStmt, LoopFor, LoopWhile,
    IfStmt, Block, Expr
)

class Interpreter:
    def __init__(self, tree: Program):
        self.tree = tree
        self.env  = {}   # name → value

    def run(self):
        self._exec_block(self.tree.statements)

    def _exec_block(self, stmts):
        for stmt in stmts:
            self._exec_stmt(stmt)

    def _exec_stmt(self, stmt):
        if isinstance(stmt, VarDecl):
            val = self._eval_expr(stmt.expr) if stmt.expr is not None else None
            self.env[stmt.name] = val

        elif isinstance(stmt, Assignment):
            val = self._eval_expr(stmt.expr)
            self.env[stmt.name] = val

        elif isinstance(stmt, WriteStmt):
            vals = [self._eval_expr(arg) for arg in stmt.args]
            print(*vals)

        elif isinstance(stmt, LoopFor):
            count = int(self._eval_expr(stmt.count))
            for i in range(count):
                self.env[stmt.var] = i
                self._exec_block(stmt.block.statements)

        elif isinstance(stmt, LoopWhile):
            while self._eval_expr(stmt.condition):
                self._exec_block(stmt.block.statements)

        elif isinstance(stmt, IfStmt):
            if self._eval_expr(stmt.condition):
                self._exec_block(stmt.block.statements)

        else:
            raise RuntimeError(f"Unhandled statement: {stmt}")

    def _eval_expr(self, expr: Expr):
        s = expr.value.replace('true','True').replace('false','False')
        s = s.replace('^','**')
        try:
            return eval(s, {}, self.env)
        except Exception as e:
            raise RuntimeError(f"Error evaluating '{expr.value}': {e}")
