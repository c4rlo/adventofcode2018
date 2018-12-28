#!/usr/bin/python

INPUT = 607331

board = [3, 7]
i, j = 0, 1

while len(board) < INPUT + 10:
    n = board[i] + board[j]
    new = []
    while n > 0:
        new.append(n % 10)
        n //= 10
    board.extend(reversed(new or [0]))
    i = (i + board[i] + 1) % len(board)
    j = (j + board[j] + 1) % len(board)

print(''.join(map(str, board[INPUT:INPUT+10])))
