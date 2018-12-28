#!/usr/bin/python

import copy
import fileinput
import sys

EMPTY = ord(b'.')
WALL = ord(b'#')
ELF = ord(b'E')
GOBLIN = ord(b'G')
UNREACHABLE = 1000000000


class Unit:
    def __init__(self, race, x, y):
        self.race = race
        self.hp = 200
        self.x = x
        self.y = y

    def pos(self):
        return self.x, self.y

    def __lt__(self, other):
        return (self.y, self.x, id(self)) < (other.y, other.x, id(other))


class Grid:
    def __init__(self, g):
        self.g = g

    def __getitem__(self, p):
        x, y = p
        return self.g[y][x]

    def __setitem__(self, p, b):
        x, y = p
        self.g[y][x] = b

    def neighbours(self, point):
        x, y = point
        if x > 0:
            yield x - 1, y
        if x < len(self.g[y]) - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < len(self.g) - 1:
            yield x, y + 1

    def empty_neighbours(self, point):
        for n in self.neighbours(point):
            if self[n] == EMPTY:
                yield n

    def distance(self, src, dst):
        frontier = {src}
        explored = set()
        i = 0
        while len(frontier) > 0:
            new_frontier = set()
            for f in frontier:
                if f == dst:
                    assert i < UNREACHABLE
                    return i
                for n in self.empty_neighbours(f):
                    if n not in frontier and n not in explored:
                        new_frontier.add(n)
            explored |= frontier
            frontier = new_frontier
            i += 1
        return UNREACHABLE


units = []
grid_ = []
for y, line in enumerate(fileinput.input()):
    row = line.rstrip('\n').encode()
    for x, cell in enumerate(row):
        if cell in (ELF, GOBLIN):
            units.append(Unit(cell, x, y))
    grid_.append(bytearray(row))
grid = Grid(grid_)

orig_units = copy.deepcopy(units)
orig_grid = copy.deepcopy(grid)


def adjacent(u1, u2):
    return abs(u1.x-u2.x) + abs(u1.y-u2.y) == 1


def enemies(unit):
    for u in units:
        if u.hp > 0 and u.race != unit.race:
            yield u


def move(unit):
    in_range = set()
    num_enemies = 0
    for enemy in enemies(unit):
        if adjacent(unit, enemy):
            # print(f"{chr(unit.race)}@{unit.x},{unit.y} already in range")
            return True
        in_range.update(grid.empty_neighbours(enemy.pos()))
        num_enemies += 1
    if num_enemies == 0:
        # print("Finished")
        return False
    if len(in_range) == 0:
        # print(f"{chr(unit.race)}@{unit.x},{unit.y} has nowhere to go")
        return True
    assert unit.pos() not in in_range
    d, y, x = min((grid.distance(unit.pos(), p), p[1], p[0]) for p in in_range)
    if d == UNREACHABLE:
        # print(f"{chr(unit.race)}@{unit.x},{unit.y} stuck")
        return True
    d, ny, nx = min((grid.distance(n, (x, y)), n[1], n[0])
                    for n in grid.empty_neighbours(unit.pos()))
    assert d != UNREACHABLE
    assert abs(unit.x-nx) + abs(unit.y-ny) == 1
    assert grid[(nx, ny)] == EMPTY
    # print(f"{chr(unit.race)}@{unit.x},{unit.y} -> {nx},{ny} for {x},{y}")
    grid[unit.pos()] = EMPTY
    unit.x = nx
    unit.y = ny
    grid[unit.pos()] = unit.race
    return True


class ElfDead(Exception):
    pass


def attack(unit, power, elflife):
    result = min(((t.hp, t.y, t.x, t)
                  for t in enemies(unit) if adjacent(unit, t)), default=None)
    if result is None:
        return
    target = result[3]
    target.hp -= power[unit.race]
    if target.hp <= 0:
        if target.race == ELF and elflife:
            raise ElfDead()
        grid[target.pos()] = EMPTY


def show(i):
    print(f"After {i} rounds:")
    uiter = iter(units)
    u = next(uiter, None)
    for y, row in enumerate(grid.g):
        print(row.decode(), end=' ')
        while u is not None and u.y == y:
            print(f"  {chr(u.race)}({u.hp})", end='')
            u = next(uiter, None)
        print()


def battle(elfpower, elflife):
    global units
    power = { GOBLIN: 3, ELF: elfpower }
    for i in range(5000000):
        units = sorted(u for u in units if u.hp > 0)
        # show(i)
        # input()
        for unit in units:
            if unit.hp > 0:
                if not move(unit):
                    units = sorted(u for u in units if u.hp > 0)
                    show(i)
                    hpsum = sum(abs(u.hp) for u in units)
                    return i * hpsum
                    # print(f"Outcome = {i} * {hpsum} = {i*hpsum}")
                    # sys.exit()
                attack(unit, power, elflife)

part1 = battle(3, False)
print("Part 1 answer:", part1)

for p in range(4, 5000000):
    units = copy.deepcopy(orig_units)
    grid = copy.deepcopy(orig_grid)
    try:
        outcome = battle(p, True)
    except ElfDead:
        pass
    else:
        print(f"Part 2 answer: With elfpower={p}, outcome={outcome}")
        break
