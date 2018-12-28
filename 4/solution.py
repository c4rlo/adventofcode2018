#!/usr/bin/python

import collections
import fileinput
import re
import sys

PREFIX_RE = re.compile(r'^\[(.{10}) (\d\d):(\d\d)\] ')
GUARD_RE = re.compile(r'Guard #(\d+) begins shift$')

guards = collections.defaultdict(list)
log = None
guard_id = None
sleep_minute = None

for line in fileinput.input():
    m = PREFIX_RE.match(line)
    date, hour, minute = m.group(1), int(m.group(2)), int(m.group(3))
    rest = line[19:]
    m = GUARD_RE.match(rest)
    if m:
        assert sleep_minute is None
        guard_id = int(m.group(1))
        log = [0] * 60
        guards[guard_id].append(log)
    elif rest == 'falls asleep\n':
        assert sleep_minute is None
        sleep_minute = minute
    elif rest == 'wakes up\n':
        assert sleep_minute is not None
        for i in range(sleep_minute, minute):
            log[i] = 1
        sleep_minute = None
    else:
        sys.exit("invalid input")

max_sleep, max_guard_id = \
    max((sum(map(sum, logs)), guard_id) for guard_id, logs in guards.items())

print(f"Guard #{max_guard_id} slept most")

logs = guards[max_guard_id]

max_sleep, max_minute = \
    max((sum(log[i] for log in logs), i) for i in range(60))

print(f"His sleepiest minute was {max_minute} ({max_sleep}x asleep)")
print("Part 1 answer:", max_guard_id * max_minute)

max_sleep, max_minute, max_guard_id = max(
    (*max((s, i) for i, s in enumerate(map(sum, zip(*logs)))), guard_id)
    for guard_id, logs in guards.items())

print("Overall sleepiest minute was "
      f"guard #{max_guard_id}'s minute {max_minute} ({max_sleep}x asleep)")
print("Part 2 answer:", max_guard_id * max_minute)
