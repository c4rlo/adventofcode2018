#!/usr/bin/python

import fileinput
import itertools

nums = [ int(ln) for ln in fileinput.input() ]
seen = set()
value = 0
for n in itertools.cycle(nums):
    value += n
    if value in seen:
        print(value)
        break
    seen.add(value)
