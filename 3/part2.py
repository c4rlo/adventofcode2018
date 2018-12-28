#!/usr/bin/python

import dataclasses
import fileinput
import re
import sys


@dataclasses.dataclass
class Rect:
    id_: int
    x: int
    y: int
    w: int
    h: int


def overlap(r1, r2):
    return overlap1d(r1.x, r1.w, r2.x, r2.w) and overlap1d(r1.y, r1.h, r2.y, r2.h)


def overlap1d(x0, w0, x1, w1):
    if x0 > x1:
        x0, w0, x1, w1 = x1, w1, x0, w0
    return x1 < x0 + w0


rects = []
overlapping = set()


LINE_RE = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')

for line in fileinput.input():
    m = LINE_RE.match(line)
    if m is None:
        sys.exit("fail @ line {}".format(fileinput.lineno()))
    g = list(map(int, m.groups()))
    r = Rect(g[0], g[1], g[2], g[3], g[4])
    for s in rects:
        if overlap(s, r):
            overlapping.add(s.id_)
            overlapping.add(r.id_)
    rects.append(r)

for r in rects:
    if r.id_ not in overlapping:
        print(r)
