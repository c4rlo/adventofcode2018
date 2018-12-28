#!/usr/bin/python

import fileinput

def close(p1, p2):
    return sum(abs(p1c - p2c) for p1c, p2c in zip(p1, p2)) <= 3

def main():
    points = { tuple( int(c) for c in line.strip().split(',') )
               for line in fileinput.input() }
    constellations = []
    while len(points) > 0:
        point = points.pop()
        layers = [[point]]
        while True:
            layer = []
            for p in points:
                if any(close(p, lp) for lp in layers[-1]):
                    layer.append(p)
            if len(layer) == 0:
                break
            points.difference_update(layer)
            layers.append(layer)
        constel = [ p for p in layer for layer in layers ]
        constellations.append(constel)
    print("Part 1 answer:", len(constellations))

main()
