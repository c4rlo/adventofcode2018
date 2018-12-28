#!/usr/bin/python

import sys

r0 = int(sys.argv[1])

r5 = 0

while True:
    r1 = r5 | 0x10000
    r5 = 10678677
    while True:
        r5 = (((r5 + (r1 & 255)) & 0xffffff) * 65899) & 0xffffff
        if r1 >= 256:
            r1 //= 256
        else:
            break
    print(r5)
    if r5 == r0:
        sys.exit()
