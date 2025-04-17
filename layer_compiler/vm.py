# vm.py

from ir import Label, Jump, JumpIfFalse

class VM:
    def __init__(self, instructions):
        self.instructions = instructions
        self.regs         = {}  # temp registers
        self.env          = {}  # variables
        # map label names to instruction indices
        self.labels = {
            instr.name: idx
            for idx, instr in enumerate(self.instructions)
            if instr.__class__.__name__ == 'Label'
        }

    def run(self):
        pc = 0
        while pc < len(self.instructions):
            instr = self.instructions[pc]
            cls   = instr.__class__.__name__

            if cls == 'LoadConst':
                self.regs[instr.target] = instr.value

            elif cls == 'LoadVar':
                self.regs[instr.target] = self.env.get(instr.name)

            elif cls == 'StoreVar':
                self.env[instr.name] = self.regs.get(instr.source)

            elif cls == 'Add':
                self.regs[instr.target] = self.regs[instr.left] + self.regs[instr.right]
            elif cls == 'Sub':
                self.regs[instr.target] = self.regs[instr.left] - self.regs[instr.right]
            elif cls == 'Mul':
                self.regs[instr.target] = self.regs[instr.left] * self.regs[instr.right]
            elif cls == 'Div':
                self.regs[instr.target] = self.regs[instr.left] / self.regs[instr.right]
            elif cls == 'Pow':
                self.regs[instr.target] = self.regs[instr.base] ** self.regs[instr.exp]

            elif cls == 'CallWrite':
                # space‑separated, no newline
                print(self.regs[instr.arg], end=' ')

            elif cls == 'PrintNewline':
                print()

            elif cls == 'Jump':
                pc = self.labels[instr.label]
                continue

            elif cls == 'JumpIfFalse':
                cond = instr.cond
                if any(op in cond for op in ('<','>','==','!=','<=','>=')):
                    cond_eval = eval(cond, {}, self.regs)
                else:
                    cond_eval = bool(self.regs.get(cond))
                if not cond_eval:
                    pc = self.labels[instr.label]
                    continue

            # LABEL is a no‑op; anything else we ignore it
            pc += 1
