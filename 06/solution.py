#!/usr/bin/python

import fileinput

points = []

for line in fileinput.input():
    x, y = map(int, line.split(','))
    points.append((x, y))

min_x = min(p[0] for p in points)
max_x = max(p[0] for p in points)
min_y = min(p[1] for p in points)
max_y = max(p[1] for p in points)

def find_closest_point_idx(x, y):
    best_dist = 1000000
    best_idx = None
    best_num = 0
    for i, p in enumerate(points):
        dist = abs(x-p[0]) + abs(y-p[1])
        if dist < best_dist:
            best_dist = dist
            best_idx = i
            best_num = 1
        elif dist == best_dist:
            best_num += 1
    if best_num == 1:
        return best_idx
    else:
        return None

area = [0] * len(points)
blacklist = set()

for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
        closest_point_idx = find_closest_point_idx(x, y)
        if closest_point_idx is not None:
            area[closest_point_idx] += 1
            if x in (min_x, max_x) or y in (min_y, max_y):
                blacklist.add(closest_point_idx)

for i in blacklist:
    area[i] = 0

print("Part 1: size of largest finite area:", max(area))

size = 0
for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
        if sum(abs(x-p[0]) + abs(y-p[1]) for p in points) < 10000:
            size += 1

print("Part 2: size of region:", size)
