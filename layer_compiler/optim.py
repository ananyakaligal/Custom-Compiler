# optim.py

import re
from ir import (
    LoadConst, LoadVar, Add, Sub, Mul, Div, Pow,
    StoreVar, CallWrite, PrintNewline,
    Label, Jump, JumpIfFalse
)

def eliminate_dead_code(ir_list):
    # 1) Collect all temps that are *used*
    used = set()
    # Any instruction with side‑effects also keeps its operands alive
    def mark_usage(instr):
        cls = instr.__class__.__name__
        if isinstance(instr, (Add, Sub, Mul, Div, Pow)):
            used.add(instr.left)
            used.add(instr.right)
        elif isinstance(instr, LoadVar):
            # source var reference
            used.add(instr.target)
        elif isinstance(instr, LoadConst):
            # target may feed a store or op
            used.add(instr.target)
        elif isinstance(instr, StoreVar):
            used.add(instr.source)
        elif isinstance(instr, CallWrite):
            used.add(instr.arg)
        elif isinstance(instr, JumpIfFalse):
            # cond could be a temp or an expression string with temps
            # find all `_t#` occurrences
            for t in re.findall(r'_t\d+', instr.cond):
                used.add(t)
        # Labels, Jumps, PrintNewline have no temps to mark here

    # First pass: mark temps used *as operands* or by side‑effects
    for instr in ir_list:
        mark_usage(instr)

    # 2) Now scan *backwards*, keeping any instr that:
    #    - has side‑effects (StoreVar, CallWrite, PrintNewline, Label, Jump, JumpIfFalse)
    #    - OR writes to a temp in `used`
    keep = [False] * len(ir_list)
    for i in range(len(ir_list) - 1, -1, -1):
        instr = ir_list[i]
        cls = instr.__class__.__name__

        is_side_effect = isinstance(instr, (StoreVar, CallWrite, PrintNewline, Label, Jump, JumpIfFalse))
        produces = getattr(instr, 'target', None)

        if is_side_effect or (produces and produces in used):
            keep[i] = True
            # if it produces a temp, now that temp is “required,”
            # we need to mark its operands too
            if isinstance(instr, (Add, Sub, Mul, Div, Pow)):
                used.add(instr.left); used.add(instr.right)
            elif isinstance(instr, StoreVar):
                used.add(instr.source)
            elif isinstance(instr, CallWrite):
                used.add(instr.arg)
            elif isinstance(instr, LoadVar) or isinstance(instr, LoadConst):
                # their target feeds something we kept
                used.add(instr.target)
            elif isinstance(instr, JumpIfFalse):
                for t in re.findall(r'_t\d+', instr.cond):
                    used.add(t)
        # else it’s dead, so we leave keep[i]=False

    # 3) Return the filtered list
    return [instr for instr, k in zip(ir_list, keep) if k]
