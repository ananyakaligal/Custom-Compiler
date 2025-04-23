# codegen.py

from layer_ast import (
    Program, VarDecl, Assignment,
    WriteStmt, LoopFor, LoopWhile, IfStmt,
    Expr
)
from ir import (
    LoadConst, LoadVar, Add, Sub, Mul, Div, Pow,
    StoreVar, CallWrite, PrintNewline,
    Label, Jump, JumpIfFalse,
    TempGenerator, LabelGenerator
)

class IRGenerator:
    def __init__(self):
        self.temp_gen  = TempGenerator()
        self.label_gen = LabelGenerator()
        self.instructions = []

    def generate(self, tree: Program):
        self.instructions = []
        for stmt in tree.statements:
            self._gen_stmt(stmt)
        return self.instructions

    def _gen_stmt(self, stmt):
        if isinstance(stmt, VarDecl):
            if stmt.expr is not None:
                src = self._gen_expr(stmt.expr)
                self.instructions.append(StoreVar(src, stmt.name))
            else:
                tmp = self.temp_gen.new_temp()
                self.instructions.append(LoadConst(None, tmp))
                self.instructions.append(StoreVar(tmp, stmt.name))

        elif isinstance(stmt, Assignment):
            src = self._gen_expr(stmt.expr)
            self.instructions.append(StoreVar(src, stmt.name))

        elif isinstance(stmt, WriteStmt):
            for expr in stmt.args:
                src = self._gen_expr(expr)
                self.instructions.append(CallWrite(src))
            self.instructions.append(PrintNewline())

        elif isinstance(stmt, LoopFor):
            start_lbl = self.label_gen.new_label("FOR_START_")
            end_lbl   = self.label_gen.new_label("FOR_END_")

            # init i = 0
            tmp0 = self.temp_gen.new_temp()
            self.instructions.append(LoadConst(0, tmp0))
            self.instructions.append(StoreVar(tmp0, stmt.var))

            # count
            cnt_tmp = self._gen_expr(stmt.count)

            # loop start
            self.instructions.append(Label(start_lbl))

            # test i < count
            i_tmp = self.temp_gen.new_temp()
            self.instructions.append(LoadVar(stmt.var, i_tmp))
            self.instructions.append(JumpIfFalse(f"{i_tmp} < {cnt_tmp}", end_lbl))

            # body
            for inner in stmt.block.statements:
                self._gen_stmt(inner)

            # i = i + 1
            curi = self.temp_gen.new_temp()
            self.instructions.append(LoadVar(stmt.var, curi))
            one  = self.temp_gen.new_temp()
            self.instructions.append(LoadConst(1, one))
            nxt  = self.temp_gen.new_temp()
            self.instructions.append(Add(curi, one, nxt))
            self.instructions.append(StoreVar(nxt, stmt.var))

            # jump back and end label
            self.instructions.append(Jump(start_lbl))
            self.instructions.append(Label(end_lbl))

        elif isinstance(stmt, LoopWhile):
            start_lbl = self.label_gen.new_label("WHILE_START_")
            end_lbl   = self.label_gen.new_label("WHILE_END_")

            self.instructions.append(Label(start_lbl))
            cond_tmp = self._gen_expr(stmt.condition)
            self.instructions.append(JumpIfFalse(cond_tmp, end_lbl))

            for inner in stmt.block.statements:
                self._gen_stmt(inner)

            self.instructions.append(Jump(start_lbl))
            self.instructions.append(Label(end_lbl))

        elif isinstance(stmt, IfStmt):
            end_lbl  = self.label_gen.new_label("IF_END_")
            cond_tmp = self._gen_expr(stmt.condition)
            self.instructions.append(JumpIfFalse(cond_tmp, end_lbl))

            for inner in stmt.block.statements:
                self._gen_stmt(inner)

            self.instructions.append(Label(end_lbl))

        else:
            raise NotImplementedError(f"IR gen not implemented for {stmt}")

    def _gen_expr(self, expr: Expr):
        v = expr.value.strip()
        # string literal
        if v.startswith('"') and v.endswith('"'):
            tmp = self.temp_gen.new_temp()
            self.instructions.append(LoadConst(v[1:-1], tmp))
            return tmp
        # numeric literal
        if v.replace('.', '', 1).lstrip('-').isdigit():
            tmp = self.temp_gen.new_temp()
            num = float(v) if '.' in v else int(v)
            self.instructions.append(LoadConst(num, tmp))
            return tmp
        # binary ops (^, then */, then +-)
        for sym, Instr in [('^', Pow), ('*', Mul), ('/', Div),
                           ('+', Add), ('-', Sub)]:
            if sym in v and not v.startswith(sym):
                left_s, right_s = v.split(sym, 1)
                left  = self._gen_expr(Expr(left_s.strip()))
                right = self._gen_expr(Expr(right_s.strip()))
                tmp   = self.temp_gen.new_temp()
                self.instructions.append(Instr(left, right, tmp))
                return tmp
        # var reference
        tmp = self.temp_gen.new_temp()
        self.instructions.append(LoadVar(v, tmp))
        return tmp
