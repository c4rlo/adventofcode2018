#!/usr/bin/python

MARBLE_MAX = 7124000
NUM_PLAYERS = 478


class Node:
    __slots__ = 'value', 'prev', 'next'

    def __init__(self, value, prev, next_):
        self.value = value
        self.prev = prev
        self.next = next_


current = Node(0, None, None)
current.prev = current
current.next = current

scores = [0] * NUM_PLAYERS
player = 0

for m in range(1, MARBLE_MAX+1):
    if m % 23 == 0:
        for _ in range(6):
            current = current.prev
        scores[player] += m + current.prev.value
        current.prev = current.prev.prev
        current.prev.next = current
    else:
        p, n = current.next, current.next.next
        current = Node(m, p, n)
        p.next = current
        n.prev = current
    player = (player + 1) % NUM_PLAYERS

print("Winning player's score:", max(scores))
