#!/usr/bin/python

import collections
import fileinput
import itertools

OPEN = ord('.')
TREE = ord('|')
LUMB = ord('#')

class Grid:
    def __init__(self, g):
        self.g = g

    def __getitem__(self, i):
        x, y = i
        try:
            return self.g[y][x]
        except IndexError:
            return None

    def __eq__(self, other):
        return self.g == other.g

    def __hash__(self):
        return hash(self.g)

    def neighbours(self, i):
        x0, y0 = i
        ylen = len(self.g)
        xlen = len(self.g[0])
        for y in range(y0 - 1, y0 + 2):
            for x in range(x0 - 1, x0 + 2):
                if (x, y) != (x0, y0) and 0 <= x < xlen and 0 <= y < ylen:
                    yield x, y


def show(grid):
    for row in grid.g:
        print(row.decode())
    print()


def acre_step(grid, i):
    a = grid[i]
    nums = collections.Counter(grid[n] for n in grid.neighbours(i))
    if a == OPEN:
        return TREE if nums[TREE] >= 3 else OPEN
    elif a == TREE:
        return LUMB if nums[LUMB] >= 3 else TREE
    elif nums[LUMB] >= 1 and nums[TREE] >= 1:
        assert a == LUMB
        return LUMB
    else:
        assert a == LUMB
        return OPEN


def step(grid):
    ylen = len(grid.g)
    xlen = len(grid.g[0])
    return Grid(tuple(bytes(acre_step(grid, (x, y)) for x in range(xlen))
                for y in range(ylen)))


def resource_value(grid):
    return sum(row.count(TREE) for row in grid.g) * \
           sum(row.count(LUMB) for row in grid.g)


def part1(grid):
    for _ in range(10):
        grid = step(grid)
    print("Part 1 answer:", resource_value(grid))


def part2(grid):
    TARGET_GEN = 1000000000
    grids = [grid]
    gens = { grid: 0 }
    for gen in itertools.count(1):
        grid = step(grid)
        prev = gens.get(grid, None)
        if prev is not None:
            print(f"Gen {prev} == gen {gen}")
            i = prev + ((TARGET_GEN - prev) % (gen - prev))
            print("Part 2 answer:", resource_value(grids[i]))
            return
        gens[grid] = gen
        grids.append(grid)


def main():
    g = []
    for line in fileinput.input():
        g.append(bytes(line.rstrip('\n').encode()))
    grid = Grid(tuple(g))
    part1(grid)
    part2(grid)


main()
