#!/usr/bin/python

import sys

r0 = int(sys.argv[1])
r1 = 0
r2 = 0
r3 = 0
r4 = 0
r5 = 0

assert r0 in (0, 1)
r2 += 2
r2 *= r2
r2 *= 19
r2 *= 11
r4 += 8
r4 *= 22
r4 += 12
r2 += r4
if r0 == 1:
    r4 = 27
    r4 *= 28
    r4 += 29
    r4 *= 30
    r4 *= 14
    r4 *= 32
    r2 += r4
    r0 = 0
r1 = 1
print(r0, r1, r2, r3, r4, r5)
