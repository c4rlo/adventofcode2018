#!/usr/bin/python

import itertools

# DEPTH = 510
# TARGET = 10, 10

DEPTH = 6969
TARGET = 9, 796

TORCH, GEAR, NEITHER = 0, 1, 2

TERRAIN_TOOLS = {TORCH, GEAR}, {GEAR, NEITHER}, {NEITHER, TORCH}

def cost_tool(terrain1, terrain2, tool):
    tools1 = TERRAIN_TOOLS[terrain1]
    tools2 = TERRAIN_TOOLS[terrain2]
    assert tool in tools1
    if tool in tools2:
        return 1, tool
    other_tool = next(t for t in tools1 if t != tool)
    assert other_tool in tools2
    return 8, other_tool


def level(gi):
    return (gi + DEPTH) % 20183


class Grid:
    def __init__(self):
        self.cache = {}

    def geoindex(self, i):
        try:
            return self.cache[i]
        except KeyError:
            gi = self._compute_geoindex(i)
            self.cache[i] = gi
            return gi

    def _compute_geoindex(self, i):
        if i == (0, 0) or i == TARGET:
            return 0
        x, y = i
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        return level(self.geoindex((x - 1, y))) * \
               level(self.geoindex((x, y - 1)))

    def terrain(self, i):
        return level(self.geoindex(i)) % 3

    def draw(self, xmax, ymax):
        icon = '.', '=', '|'
        for y in range(ymax + 1):
            for x in range(xmax + 1):
                print(icon[self.terrain((x, y))], end='')
            print()

    def neighbours(self, i):
        x, y = i
        if y > 0:
            yield x, y - 1
        if x > 0:
            yield x - 1, y
        yield x, y + 1
        yield x + 1, y

    def find_route(self):
        candidate = None
        explored = set((0, 0, TORCH))
        frontiers = [
            # TORCH
            { (0, 0): 0 },
            # GEAR
            {},
            # NEITHER
            {}
        ]
        for max_cost in itertools.count(1):
            new_frontiers = [{},{},{}]
            for tool, frontier in enumerate(frontiers):
                for pos, pos_cost in frontier.items():
                    pos_terrain = self.terrain(pos)
                    done = True
                    for n in self.neighbours(pos):
                        c, t = cost_tool(pos_terrain, self.terrain(n), tool)
                        if (*n, t) not in explored:
                            n_cost = pos_cost + c
                            if n_cost <= max_cost:
                                assert n_cost == max_cost
                                if n == TARGET:
                                    total_cost = n_cost
                                    if t != TORCH:
                                        assert t == GEAR
                                        total_cost += 7
                                    if candidate is not None:
                                        return min(candidate, total_cost)
                                    candidate = total_cost
                                new_frontiers[t][n] = n_cost
                                explored.add((*n, t))
                            else:
                                done = False
                    if not done:
                        new_frontiers[tool][pos] = pos_cost
            frontiers = new_frontiers
            for tool, frontier in enumerate(frontiers):
                for pos in frontier.keys():
                    explored.add((*pos, tool))


def part1(grid):
    width = TARGET[0] + 1
    height = TARGET[1] + 1

    total_risk = sum(grid.terrain((x, y))
                     for x in range(width) for y in range(height))
    print("Part 1 answer:", total_risk)


def part2(grid):
    # grid.draw(15, 15)
    cost = grid.find_route()
    print("Part 2 answer:", cost)


def main():
    grid = Grid()
    part1(grid)
    part2(grid)

main()
