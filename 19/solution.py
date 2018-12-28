#!/usr/bin/python

import fileinput


class Op:
    def __init__(self, f, symbol, assign_symbol):
        self.f = f
        self.symbol = symbol
        self.assign_symbol = assign_symbol


def op(symbol=None, assign_symbol=None):
    def wrapped(f):
        return Op(f, symbol, assign_symbol)
    return wrapped


@op('+', '+=')
def op_add(a, b): return a + b

@op('*', '*=')
def op_mul(a, b): return a * b

@op('&', '&=')
def op_ban(a, b): return a & b

@op('|', '|=')
def op_bor(a, b): return a | b

@op()
def op_set(a, b): return a

@op('>')
def op_gt(a, b): return 1 if a > b else 0

@op('==')
def op_eq(a, b): return 1 if a == b else 0


LHS, RHS = 0, 1


def imm_value(arg, regs):
    return arg

def imm_str(arg, side, reginfo):
    return str(arg)

arg_imm = imm_value, imm_str


def reg_value(arg, regs):
    return regs[arg]

def reg_str(arg, side, reginfo):
    try:
        return str(reginfo[arg][side])
    except KeyError:
        return f"r{arg}"

arg_reg = reg_value, reg_str


class Inst:
    def __init__(self, op, arg1fn, arg2fn):
        self.op = op
        self.arg1fn = arg1fn
        self.arg2fn = arg2fn

    def execute(self, regs, arg1, arg2):
        a1 = self.arg1fn[0](arg1, regs)
        if self.arg2fn is not None:
            a2 = self.arg2fn[0](arg2, regs)
        else:
            a2 = None
        return self.op.f(a1, a2)

    def str(self, arg1, arg2, dest_reg, reginfo):
        dest_str = reg_str(dest_reg, LHS, reginfo)
        a1 = self.arg1fn[1](arg1, RHS, reginfo)
        if self.arg2fn is None:
            return f"{dest_str} = {a1}"
        a2 = self.arg2fn[1](arg2, RHS, reginfo)
        if self.op.assign_symbol is not None:
            if self.arg1fn == arg_reg and arg1 == dest_reg:
                return f"{dest_str} {self.op.assign_symbol} {a2}"
            if self.arg2fn == arg_reg and arg2 == dest_reg:
                # rely on commutativity of all ops
                return f"{dest_str} {self.op.assign_symbol} {a1}"
        return f"{dest_str} = {a1} {self.op.symbol} {a2}"


instructions = {
    'addr': Inst(op_add, arg_reg, arg_reg),
    'addi': Inst(op_add, arg_reg, arg_imm),
    'mulr': Inst(op_mul, arg_reg, arg_reg),
    'muli': Inst(op_mul, arg_reg, arg_imm),
    'banr': Inst(op_ban, arg_reg, arg_reg),
    'bani': Inst(op_ban, arg_reg, arg_imm),
    'borr': Inst(op_bor, arg_reg, arg_reg),
    'bori': Inst(op_bor, arg_reg, arg_imm),
    'setr': Inst(op_set, arg_reg, None),
    'seti': Inst(op_set, arg_imm, None),
    'gtir': Inst(op_gt, arg_imm, arg_reg),
    'gtri': Inst(op_gt, arg_reg, arg_imm),
    'gtrr': Inst(op_gt, arg_reg, arg_reg),
    'eqir': Inst(op_eq, arg_imm, arg_reg),
    'eqri': Inst(op_eq, arg_reg, arg_imm),
    'eqrr': Inst(op_eq, arg_reg, arg_reg)
}


def run(program, ipreg, r0):
    regs = [0] * 6
    regs[0] = r0
    ip = 0
    while 0 <= ip < len(program):
        # print(regs)
        inst, a, b, dest = program[ip]
        regs[dest] = inst.execute(regs, a, b)
        # print(regs)
        # print()
        regs[ipreg] += 1
        ip = regs[ipreg]
    return regs


def disasm(program, ipreg, r0):
    for i, op in enumerate(program):
        inst, a, b, dest = op
        reginfo = { ipreg: ('ip', i) }
        s = inst.str(a, b, dest, reginfo)
        if dest == ipreg:
            jump = "; jump ip+1"
        else:
            jump = ""
        print(f"{i:2d}: {s}{jump}")


def main():
    ipreg = None
    program = []
    for line in fileinput.input():
        if line.startswith('#ip '):
            ipreg = int(line[4:])
        else:
            inst, *args = line.split()
            program.append((instructions[inst], *map(int, args)))
    regs = run(program, ipreg, 0)
    print("Part 1:", regs)
    print()
    disasm(program, ipreg, 1)


main()
