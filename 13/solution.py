#!/usr/bin/python

import fileinput
import numpy as np
import sys


UP = np.array((0, -1))
DOWN = np.array((0, 1))
LEFT = np.array((-1, 0))
RIGHT = np.array((1, 0))

STRAIGHT = np.eye(2, dtype=int)
TURN_LEFT = np.array(((0, 1), (-1, 0)))
TURN_RIGHT = np.array(((0, -1), (1, 0)))
XINGMOD = TURN_LEFT, STRAIGHT, TURN_RIGHT

CART_SYMBOLS = {
    ord('^'): (UP, ord('|')),
    ord('v'): (DOWN, ord('|')),
    ord('<'): (LEFT, ord('-')),
    ord('>'): (RIGHT, ord('-'))
}


class Cart:
    def __init__(self, x, y, direction):
        self.tick = 0
        self.x = x
        self.y = y
        self.direction = direction
        self.xingmodidx = 0

    def __lt__(self, other):
        return (self.tick, self.y, self.x) < (other.tick, other.y, other.x)


carts = {}
grid = None

for y, line in enumerate(fileinput.input()):
    line = np.copy(np.frombuffer(line.rstrip('\n').encode(), dtype=np.ubyte))
    for x, b in enumerate(line):
        if b in CART_SYMBOLS:
            direction, track = CART_SYMBOLS[b]
            carts[(x, y)] = Cart(x, y, direction)
            line[x] = track
    if grid is None:
        grid = line
    else:
        grid = np.vstack((grid, line))


def draw():
    map_ = np.copy(grid)
    for cart in carts:
        c = None
        d = cart.direction
        if np.array_equal(d, UP):
            c = '^'
        elif np.array_equal(d, DOWN):
            c = 'v'
        elif np.array_equal(d, LEFT):
            c = '<'
        elif np.array_equal(d, RIGHT):
            c = '>'
        else:
            sys.exit("Bad cart direction")
        map_[cart.y, cart.x] = ord(c)
    for y in range(len(map_)):
        for x in range(len(map_[y])):
            print(chr(map_[y, x]), end='')
        print()


while True:
    cart = min(carts.values())
    if len(carts) == 1:
        print(f"Last cart location (pre): {cart.x},{cart.y}")
    del carts[(cart.x, cart.y)]
    d = cart.direction
    assert d.shape == (2,)
    cart.x += d[0]
    cart.y += d[1]
    if (cart.x, cart.y) in carts:
        print(f"Crash at {cart.x},{cart.y}")
        del carts[(cart.x, cart.y)]
        continue
    carts[(cart.x, cart.y)] = cart
    c = chr(grid[cart.y, cart.x])
    assert len(c) == 1
    if c == '\\' and (np.array_equal(d, LEFT) or np.array_equal(d, RIGHT)):
        d = TURN_RIGHT @ d
    elif c == '\\' and (np.array_equal(d, UP) or np.array_equal(d, DOWN)):
        d = TURN_LEFT @ d
    elif c == '/' and (np.array_equal(d, LEFT) or np.array_equal(d, RIGHT)):
        d = TURN_LEFT @ d
    elif c == '/' and (np.array_equal(d, UP) or np.array_equal(d, DOWN)):
        d = TURN_RIGHT @ d
    elif c == '|' and (np.array_equal(d, UP) or np.array_equal(d, DOWN)):
        pass
    elif c == '-' and (np.array_equal(d, LEFT) or np.array_equal(d, RIGHT)):
        pass
    elif c == '+':
        d = XINGMOD[cart.xingmodidx] @ d
        cart.xingmodidx = (cart.xingmodidx + 1) % len(XINGMOD)
    else:
        sys.exit(f"Bad state: tick={cart.tick}, xy={cart.x},{cart.y}, c={c}, d={d}")
    cart.direction = d
    cart.tick += 1
    if len(carts) == 1:
        print(f"Last cart location (post): {cart.x},{cart.y}")
        sys.exit()
    # draw()
    # input()
