#!/usr/bin/python

import sys

INPUT = [ 6, 0, 7, 3, 3, 1 ]

board = [3, 7]
i, j = 0, 1

while True:
    n = board[i] + board[j]
    new = []
    while n > 0:
        new.append(n % 10)
        n //= 10
    new.reverse()
    if len(new) == 0:
        new = [0]
    for k in new:
        board.append(k)
        if board[-len(INPUT):] == INPUT:
            print("Part 2 answer:", len(board) - len(INPUT))
            sys.exit()
    i = (i + board[i] + 1) % len(board)
    j = (j + board[j] + 1) % len(board)
