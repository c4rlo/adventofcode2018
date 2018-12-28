#!/usr/bin/python

SERIAL = 5034

def range2d(xmin, xmax, ymin, ymax):
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            yield x, y


power = { (x, y): ((((x+10)*y+SERIAL)*(x+10) // 100) % 10) - 5
          for (x, y) in range2d(1, 301, 1, 301) }

_, x, y = max((sum(power[c] for c in range2d(x, x+3, y, y+3)), x, y)
              for (x, y) in range2d(1, 298, 1, 298))

print(f"Part 1 answer: {x},{y}")


cumul = {}
for x in range(1, 301):
    ysum = 0
    for y in range(1, 301):
        ysum += power[(x, y)]
        cumul[(x, y)] = cumul.get((x-1, y), 0) + ysum


def c(x, y):
    return cumul.get((x-1, y-1), 0)


_, x, y, s = \
    max((c(x+s, y+s) - c(x+s, y) - c(x, y+s) + c(x, y), x, y, s)
        for s in range(1, 301)
        for (x, y) in range2d(1, 301-s, 1, 301-s))

print(f"Part 2 answer: {x},{y},{s}")
