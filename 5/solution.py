#!/usr/bin/python

import string

polymer = open('input', 'rb').read().rstrip()
initial_len = len(polymer)
print("Initial length:", initial_len)

def reacted_len(poly):
    p = bytearray(poly)
    imin = 1
    while True:
        for i in range(imin, len(p)):
            a, b = p[i-1], p[i]
            if a ^ b == 0x20:
                del p[i-1:i+1]
                imin = max(i-1, 1)
                break
        else:
            break
    return len(p)

print("Reacted length:", reacted_len(polymer))

best_len = initial_len
best_unit = None
for v in string.ascii_lowercase:
    u = bytes(v, encoding='ascii')
    l = reacted_len(polymer.replace(u, b'').replace(u.upper(), b''))
    if l < best_len:
        best_len = l
        best_unit = u

print(f"After removing '{best_unit.decode()}', reacted length: {best_len}")
