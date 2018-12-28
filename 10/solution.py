#!/usr/bin/python

import fileinput
import re

LINE_RE = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)>\s*velocity=<\s*(-?\d+),\s*(-?\d+)>$')

points = {}

for line in fileinput.input():
    m = LINE_RE.match(line)
    x, y, vx, vy = map(int, m.group(1, 2, 3, 4))
    points[(x, y)] = (vx, vy)

for i in range(10639):
    points = { (x+vx, y+vy): (vx, vy) for (x, y), (vx, vy) in points.items() }

for y in range(166, 178):
    for x in range(181, 244):
        if (x, y) in points:
            print('#', end='')
        else:
            print('.', end='')
    print()


# prev_dim_x = 1_000_000_000
# prev_dim_y = 1_000_000_000
# countdown = -1

# for i in range(20000):
#     min_x = min(x for (x, y) in points)
#     max_x = max(x for (x, y) in points)
#     min_y = min(y for (x, y) in points)
#     max_y = max(y for (x, y) in points)
#     dim_x = max_x - min_x
#     dim_y = max_y - min_y
#     if countdown == -1 and (dim_x >= prev_dim_x or dim_y >= prev_dim_y):
#         countdown = 10
#     if countdown > 0:
#         print(f"i={i}: {dim_x}x{dim_y} ({min_x},{min_y})")
#         countdown -= 1
#     elif i >= 10630:
#         print(f"i={i}: {dim_x}x{dim_y} ({min_x},{min_y})")
#     if countdown == 0:
#         break
#     points = { (x+vx, y+vy): (vx, vy) for (x, y), (vx, vy) in points.items() }
#     prev_dim_x = dim_x
#     prev_dim_y = dim_y
