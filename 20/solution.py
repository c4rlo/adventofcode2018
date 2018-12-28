#!/usr/bin/python

import sys

class Choice:
    def __init__(self, branches):
        self.branches = branches

    def build_doors(self, start, grid):
        return set.union(*(branch.build_doors(start, grid)
                           for branch in self.branches))


class Sequence:
    def __init__(self, elements):
        self.elements = elements

    def build_doors(self, start, grid):
        ends = {start}
        for elem in self.elements:
            ends = set.union(*(elem.build_doors(pos, grid) for pos in ends))
        return ends


class Direction:
    def __init__(self, d):
        self.d = d

    def build_doors(self, start, grid):
        x, y = start
        if self.d == 'N':
            grid.doors_south.add((x, y - 1))
            y -= 1
        elif self.d == 'S':
            grid.doors_south.add((x, y))
            y += 1
        elif self.d == 'W':
            grid.doors_east.add((x - 1, y))
            x -= 1
        elif self.d == 'E':
            grid.doors_east.add((x, y))
            x += 1
        else:
            raise RuntimeError("bad direction")
        return {(x, y)}


class Grid:
    def __init__(self):
        self.doors_east = set()
        self.doors_south = set()

    def draw(self, start):
        xmin = min(min(x for x, y in self.doors_east),
                   min(x for x, y in self.doors_south))
        xmax = max(max(x + 1 for x, y in self.doors_east),
                   max(x for x, y in self.doors_south))
        ymin = min(min(y for x, y in self.doors_east),
                   min(y for x, y in self.doors_south))
        ymax = max(max(y for x, y in self.doors_east),
                   max(y + 1 for x, y in self.doors_south))
        print('#' * ((xmax - xmin + 1) * 2 + 1))
        for y in range(ymin, ymax + 1):
            line = '#'
            for x in range(xmin, xmax + 1):
                line += ('X' if (x, y) == start else '.')
                line += ('|' if (x, y) in self.doors_east else '#')
            print(line)
            line = '#'
            for x in range(xmin, xmax + 1):
                line += ('-' if (x, y) in self.doors_south else '#')
                line += '#'
            print(line)

    def neighbours(self, pos):
        x, y = pos
        if (x, y) in self.doors_east:
            yield x + 1, y
        if (x - 1, y) in self.doors_east:
            yield x - 1, y
        if (x, y) in self.doors_south:
            yield x, y + 1
        if (x, y - 1) in self.doors_south:
            yield x, y - 1

    def furthest_away(self, start):
        explored = set()
        frontier = {start}
        steps = 0
        while len(frontier) > 0:
            new_frontier = set()
            for f in frontier:
                for n in self.neighbours(f):
                    if n not in frontier and n not in explored:
                        new_frontier.add(n)
            explored |= frontier
            frontier = new_frontier
            steps += 1
        return steps - 1

    def count_far_locations(self, start, min_doors):
        explored = set()
        frontier = {start}
        count = 0
        steps = 0
        while len(frontier) > 0:
            new_frontier = set()
            for f in frontier:
                for n in self.neighbours(f):
                    if n not in frontier and n not in explored:
                        new_frontier.add(n)
            explored |= frontier
            frontier = new_frontier
            steps += 1
            if steps >= min_doors:
                count += len(frontier)
        return count


def parse_sequence(regex):
    elements = []
    while True:
        c = regex[0]
        if c in 'NEWS':
            elements.append(Direction(c))
            regex = regex[1:]
        elif c == '(':
            choice, regex = parse_choice(regex[1:])
            assert regex[0] == ')'
            regex = regex[1:]
            elements.append(choice)
        else:
            return Sequence(elements), regex

def parse_choice(regex):
    branches = []
    while True:
        seq, regex = parse_sequence(regex)
        branches.append(seq)
        if regex[0] != '|':
            return Choice(branches), regex
        regex = regex[1:]

def main():
    regex = open(sys.argv[1]).read().rstrip("\n")
    assert regex[0] == '^'
    choice, rest = parse_choice(regex[1:])
    assert rest == '$'
    grid = Grid()
    start = 0, 0
    choice.build_doors(start, grid)
    # grid.draw(start)
    steps = grid.furthest_away(start)
    print(f"Part 1 answer: furthest room requires passing {steps} doors.")
    num_far = grid.count_far_locations(start, 1000)
    print(f"Part 2 answer: {num_far} locations are >= 1000 doors away.")

main()
