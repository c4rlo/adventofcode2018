#!/usr/bin/python

import fileinput
import functools
import operator
import re


def in_range(p0, r0, p1):
    return sum(abs(a - b) for (a, b) in zip(p0, p1)) <= r0

def part1(bots):
    best_radius, best_pos = max((r, pos) for (pos, r) in bots)

    count = sum(1 if in_range(best_pos, best_radius, pos) else 0
                for pos, _ in bots)

    print("Part 1 answer:", count)


class Range:  # inclusive range
    def __init__(self, min_, max_):
        self.min_ = min_
        self.max_ = max_

    def __and__(self, other):  # intersect
        if self.min_ > other.min_:
            return other & self
        if other.min_ <= self.max_:
            return Range(other.min_, self.max_)
        return None

    def __str__(self):
        return f"{self.min_}..{self.max_}"


class Region:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def from_xyzr(x, y, z, r):
        a = x+y+z
        b = x+y-z
        c = x-y+z
        d = x-y-z
        def rr(e): return Range(e-r, e+r)
        return Region(rr(a), rr(b), rr(c), rr(d))

    def __and__(self, other):  # intersect
        dims = (self.a & other.a, self.b & other.b,
                self.c & other.c, self.d & other.d)
        if all(dims):
            return Region(*dims)
        return None

    def vertices_xyz(self):
        result = set()

        for a in (self.a.min_, self.a.max_):
            for b in (self.b.min_, self.b.max_):
                for c in (self.c.min_, self.c.max_):
                    x, y, z = (b+c)/2, (a-c)/2, (a-b)/2
                    d = x - y - z
                    if self.d.min_ <= d <= self.d.max_:
                        result.add((x, y, z))

        for a in (self.a.min_, self.a.max_):
            for b in (self.b.min_, self.b.max_):
                for d in (self.d.min_, self.d.max_):
                    x, y, z = (a+d)/2, (b-d)/2, (a-b)/2
                    c = x - y + z
                    if self.c.min_ <= c <= self.c.max_:
                        result.add((x, y, z))

        # We should possibly also iterate over (a, c, d) and (b, c, d)
        # tuples; not sure. In practice, we find all 8 vertices with just the
        # above.

        print(f"Got {len(result)} vertices")

        return result

    def distance_from_origin(self):
        return min(sum(abs(d) for d in xyz) for xyz in self.vertices_xyz())

    def __str__(self):
        return f"{self.a} {self.b} {self.c} {self.d}"


def part2(bots):
    regions = [ Region.from_xyzr(*pos, r) for (pos, r) in bots ]
    clusters = [ (i,) for i in range(len(regions)) ]
    while True:
        new_clusters = []
        for cluster in clusters:
            last = cluster[-1]
            for ridx in range(last+1, len(regions)):
                region = regions[ridx]
                if all(region & regions[i] for i in cluster):
                    new_clusters.append((*cluster, ridx))
                break
        if len(new_clusters) == 0:
            break
        clusters = new_clusters
        # print(f"Found {len(clusters)} {len(clusters[0])}-tuples")
    for cluster in clusters:
        # print("Cluster:", cluster)
        intersection = functools.reduce(operator.and_,
                                        (regions[i] for i in cluster))
        print("Intersection:", intersection)
        print("Part 2 answer (distance from origin):",
              intersection.distance_from_origin())


def main():
    bots = []

    LINE_RE = re.compile(r'^pos=<(-?\d+),(-?\d+),(-?\d+)>,\s*r=(\d+)$')
    for line in fileinput.input():
        m = LINE_RE.match(line)
        pos = list(map(int, m.group(1, 2, 3)))
        radius = int(m.group(4))
        bots.append((pos, radius))

    part1(bots)
    part2(bots)

main()
