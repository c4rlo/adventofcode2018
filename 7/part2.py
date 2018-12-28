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

log = []
time = 0
workers = [0] * 5

while len(depends) > 0:
    while True:
        step = min((s for s, b in depends.items() if len(b) == 0), default=None)
        if step is None:
            break
        del depends[step]
        min_w, min_i = min((w, i) for i, w in enumerate(workers))
        endtime = max(time, min_w) + 60 + ord(step) - ord('A') + 1
        workers[min_i] = endtime
        log.append((endtime, step))
        log.sort()
    if len(log) == 0:
        break
    time, step = log[0]
    log = log[1:]
    for d in depends.values():
        d.discard(step)

print("Part 2 answer:", time)
