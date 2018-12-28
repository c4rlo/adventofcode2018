#!/usr/bin/python

import fileinput
import re
import sys


SAND = ord(b'.')
CLAY = ord(b'#')
WATER = ord(b'~')
TOUCHED = ord(b'|')

PASSABLE = SAND, TOUCHED
IMPASSABLE = CLAY, WATER


class Grid:
    def __init__(self, value, xmin, xmax, ymin, ymax):
        empty_row = bytes([value] * (xmax - xmin + 1))
        self.g = [ bytearray(empty_row) for _ in range(ymax - ymin + 1) ]
        self.xmin = xmin
        self.ymin = ymin

    def __getitem__(self, i):
        x, y = i
        try:
            return self.g[y - self.ymin][x - self.xmin]
        except IndexError:
            return None

    def __setitem__(self, i, v):
        x, y = i
        self.g[y - self.ymin][x - self.xmin] = v


def read_grid(f):
    LINE_RE = re.compile(r'^([xy])=(\d+),\s*([xy])=(\d+)\.\.(\d+)$')

    clay = []
    for line in f:
        m = LINE_RE.match(line)
        v1, a = m.group(1), int(m.group(2))
        v2, b, c = m.group(3), int(m.group(4)), int(m.group(5))
        if v1 == 'x' and v2 == 'y':
            clay.append((a, a, b, c))
        elif v1 == 'y' and v2 == 'x':
            clay.append((b, c, a, a))

    clay_xmin = min(c[0] for c in clay)
    clay_xmax = max(c[1] for c in clay)
    clay_ymin = min(c[2] for c in clay)
    clay_ymax = max(c[3] for c in clay)

    grid = Grid(SAND, clay_xmin - 1, clay_xmax + 1, clay_ymin, clay_ymax)

    for xmin, xmax, ymin, ymax in clay:
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                grid[x, y] = CLAY

    return grid


def show(grid):
    for row in grid.g:
        print(row.decode())
    print()


deadends = set()

LEDGE, WALL, DEADEND = 0, 1, 2


def drop(grid, x, y):
    assert grid[x, y] in PASSABLE
    grid[x, y] = TOUCHED
    while grid[x, y + 1] in PASSABLE:
        y += 1
        grid[x, y] = TOUCHED
    return x, y


def explore_horizontal(grid, x, y, xinc):
    while grid[x + xinc, y + 1] in IMPASSABLE and \
            grid[x + xinc, y] in PASSABLE:
        x += xinc
        grid[x, y] = TOUCHED
    if (x + xinc, y) in deadends:
        return DEADEND, x
    elif grid[x + xinc, y] in IMPASSABLE:
        return WALL, x
    else:
        return LEDGE, x


def trickle(grid):
    x, y = 500, grid.ymin
    if (x, y) in deadends:
        return False
    lastfork = None
    while True:
        predrop = x, y
        x, y = drop(grid, x, y)
        if grid[x, y + 1] is None:
            deadends.add(predrop)
            return True
        left, xleft = explore_horizontal(grid, x, y, -1)
        right, xright = explore_horizontal(grid, x, y, 1)
        if left == right == LEDGE:
            lastfork = predrop
        if left == right == WALL:
            wx = xleft if xleft != x else xright
            assert grid[wx, y] in PASSABLE
            grid[wx, y] = WATER
            return True
        elif left == LEDGE:
            x = xleft - 1
        elif right == LEDGE:
            x = xright + 1
        elif lastfork is None:
            return False
        else:
            deadends.add(predrop)
            return True


grid = read_grid(fileinput.input())
# show(grid)
# sys.exit()

while True:
    # show(grid)
    # input()
    if not trickle(grid):
        break

# show(grid)
print("Part 1 answer:",
      sum(row.count(b) for row in grid.g for b in (WATER, TOUCHED)))
print("Part 2 answer:",
      sum(row.count(WATER) for row in grid.g))
