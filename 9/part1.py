#!/usr/bin/python

MARBLE_MAX = 71240
NUM_PLAYERS = 478

marbles = [0]
current = 0
scores = [0] * NUM_PLAYERS
player = 0

for m in range(1, MARBLE_MAX+1):
    if m % 23 == 0:
        current = (current - 7 + len(marbles)) % len(marbles)
        scores[player] += m + marbles[current]
        del marbles[current]
    else:
        current = (current + 2) % len(marbles)
        marbles.insert(current, m)
    player = (player + 1) % NUM_PLAYERS

print("Winning player's score:", max(scores))
