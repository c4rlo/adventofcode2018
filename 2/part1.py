#!/usr/bin/python

import fileinput
import collections

twos = 0
threes = 0

for line in fileinput.input():
    counts = list(collections.Counter(line.rstrip('\n')).values())
    if 2 in counts:
        twos += 1
    if 3 in counts:
        threes += 1

print("twos={}, threes={}, checksum={}".format(twos, threes, twos*threes))
