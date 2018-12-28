#!/usr/bin/python

import fileinput
import re
import sys

LINE_RE = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')

fabric = []

def ensure_len(ls, n, ty):
    for _ in range(len(ls), n):
        ls.append(ty())

for line in fileinput.input():
    m = LINE_RE.match(line)
    if m is None:
        sys.exit("fail @ line {}".format(fileinput.lineno()))
    g = list(map(int, m.groups()))
    x0, y0, w, h = g[1], g[2], g[3], g[4]
    ensure_len(fabric, x0+w, list)
    for x in range(x0, x0+w):
        fx = fabric[x]
        ensure_len(fx, y0+h, int)
        for y in range(y0, y0+h):
            fx[y] += 1

answer = 0
for row in fabric:
    for e in row:
        if e > 1:
            answer += 1

print(answer)
