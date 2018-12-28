#!/usr/bin/python

import collections
import fileinput
import re

depends = collections.defaultdict(set)

LINE_RE = re.compile(r'Step (\w+) must be finished before step (\w+) can begin\.$')

for line in fileinput.input():
    m = LINE_RE.match(line)
    dep, step = m.group(1), m.group(2)
    depends[step].add(dep)
    depends[dep]  # ensure exists

order = ''

while len(depends) > 0:
    step = min((s for s, b in depends.items() if len(b) == 0))
    del depends[step]
    for b in depends.values():
        b.discard(step)
    order += step

print("Part 1 answer:", order)
