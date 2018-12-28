#!/usr/bin/python

import fileinput
import sys

lines = list(map(str.rstrip, fileinput.input()))
for i in range(len(lines[0])):
    seen = set()
    for line in lines:
        s = line[:i] + line[(i+1):]
        if s in seen:
            print(s)
            sys.exit()
        seen.add(s)
