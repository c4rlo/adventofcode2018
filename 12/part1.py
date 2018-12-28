#!/usr/bin/python

import re

ON_RULE_RE = re.compile(r'([.#]{5}) => #$')

f = open('input')
state_str = re.match(r'initial state: ([.#]+)$', f.readline()).group(1)
state = set(i for (i, s) in enumerate(state_str) if s == '#')

rule = set()
for line in f:
    m = ON_RULE_RE.match(line)
    if m:
        code = sum(1 << i for (i, s) in enumerate(m.group(1)) if s == '#')
        rule.add(code)

i_min, i_max = 0, len(state_str) - 1
for _ in range(20):
    r = range(i_min - 2, i_max + 3)
    i_min, i_max = 1000000, -1000000
    state_new = set()
    for i in r:
        code = sum(1 << j for j in range(5) if i+j-2 in state)
        if code in rule:
            state_new.add(i)
            i_min, i_max = min(i_min, i), max(i_max, i)
    state = state_new

print("Part 1 answer:", sum(state))
