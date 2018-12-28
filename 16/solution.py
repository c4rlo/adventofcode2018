#!/usr/bin/python

import re
import sys

BEFORE_RE = re.compile(r'^Before:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]$')
INST_RE = re.compile(r'^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$')
AFTER_RE = re.compile(r'^After:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]$')

def addr(reg, a, b): return reg[a] + reg[b]
def addi(reg, a, b): return reg[a] + b
def mulr(reg, a, b): return reg[a] * reg[b]
def muli(reg, a, b): return reg[a] * b
def banr(reg, a, b): return reg[a] & reg[b]
def bani(reg, a, b): return reg[a] & b
def borr(reg, a, b): return reg[a] | reg[b]
def bori(reg, a, b): return reg[a] | b
def setr(reg, a, b): return reg[a]
def seti(reg, a, b): return a
def gtir(reg, a, b): return 1 if a > reg[b] else 0
def gtri(reg, a, b): return 1 if reg[a] > b else 0
def gtrr(reg, a, b): return 1 if reg[a] > reg[b] else 0
def eqir(reg, a, b): return 1 if a == reg[b] else 0
def eqri(reg, a, b): return 1 if reg[a] == b else 0
def eqrr(reg, a, b): return 1 if reg[a] == reg[b] else 0

instructions = [
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, gtri, gtrr,
    eqir, eqri, eqrr
]

def call(inst, args, reg):
    a, b, c = args
    creg = reg[:]
    creg[c] = inst(creg, a, b)
    return creg

def num_opcodes(args, before, after):
    return sum(1 for i in instructions if call(i, args, before) == after)

possible = {}
answer1 = 0

f = open(sys.argv[1])

while True:
    m = BEFORE_RE.match(f.readline())
    if m is None:
        break
    before = list(map(int, m.groups()))
    m = INST_RE.match(f.readline())
    op, *args = list(map(int, m.groups()))
    m = AFTER_RE.match(f.readline())
    after = list(map(int, m.groups()))
    if num_opcodes(args, before, after) >= 3:
        answer1 += 1
    if op not in possible:
        possible[op] = set(instructions)
    for i in instructions:
        if call(i, args, before) != after:
            possible[op].discard(i)
    line = f.readline()
    assert len(line.strip()) == 0

print("Part 1 answer:", answer1)

opcodes = {}
while len(opcodes) < 16:
    for op, i in opcodes.items():
        for ins in possible.values():
            ins.discard(i)
    for op, ins in possible.items():
        if len(ins) == 1:
            opcodes[op] = ins.pop()
    possible = { op: ins for op, ins in possible.items() if len(ins) > 1 }

# for op, i in opcodes.items():
#     print(f"{op}: {i.__name__}")

reg = [0, 0, 0, 0]
for line in f:
    if len(line.strip()) == 0:
        continue
    op, *args = map(int, line.split())
    reg = call(opcodes[op], args, reg)

# print(reg)
print("Part 2 answer:", reg[0])
