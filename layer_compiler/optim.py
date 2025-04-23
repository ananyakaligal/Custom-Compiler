import re
from ir import (
    LoadConst, LoadVar, Add, Sub, Mul, Div, Pow,
    StoreVar, CallWrite, PrintNewline,
    Label, Jump, JumpIfFalse
)

def eliminate_dead_code(ir_list):
    # 1) Collect all temps that are *used*
    used = set()

    def mark_usage(instr):
        # Add operands of instructions with side-effects
        if isinstance(instr, (Add, Sub, Mul, Div)):
            used.add(instr.left)
            used.add(instr.right)
        elif isinstance(instr, Pow):
            used.add(instr.base)
            used.add(instr.exp)
        elif isinstance(instr, LoadVar):
            used.add(instr.target)
        elif isinstance(instr, LoadConst):
            used.add(instr.target)
        elif isinstance(instr, StoreVar):
            used.add(instr.source)
        elif isinstance(instr, CallWrite):
            used.add(instr.arg)
        elif isinstance(instr, JumpIfFalse):
            for t in re.findall(r'_t\d+', instr.cond):
                used.add(t)
        # Labels, Jumps, PrintNewline have no temps to mark here

    # First pass: mark temps used *as operands* or by side‑effects
    for instr in ir_list:
        mark_usage(instr)

    # 2) Scan backward and keep:
    # - Side-effect instructions
    # - Any instruction producing a temp in 'used'
    keep = [False] * len(ir_list)
    for i in range(len(ir_list) - 1, -1, -1):
        instr = ir_list[i]
        produces = getattr(instr, 'target', None)
        is_side_effect = isinstance(instr, (
            StoreVar, CallWrite, PrintNewline,
            Label, Jump, JumpIfFalse
        ))

        if is_side_effect or (produces and produces in used):
            keep[i] = True

            # Propagate operand usage
            if isinstance(instr, (Add, Sub, Mul, Div)):
                used.add(instr.left)
                used.add(instr.right)
            elif isinstance(instr, Pow):
                used.add(instr.base)
                used.add(instr.exp)
            elif isinstance(instr, StoreVar):
                used.add(instr.source)
            elif isinstance(instr, CallWrite):
                used.add(instr.arg)
            elif isinstance(instr, (LoadVar, LoadConst)):
                used.add(instr.target)
            elif isinstance(instr, JumpIfFalse):
                for t in re.findall(r'_t\d+', instr.cond):
                    used.add(t)

    # 3) Return pruned instructions
    return [instr for instr, keep_flag in zip(ir_list, keep) if keep_flag]
