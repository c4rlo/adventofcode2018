#!/usr/bin/python

import copy
import fileinput
import re

LINE_RE = re.compile(
    r'^(\d+) units each with (\d+) hit points (?:\(([^)]+)\) )?'
    r'with an attack that does (\d+) (\w+) damage at initiative (\d+)$')


class Group:
    def __init__(self, army_idx, units, hp, damage, attack, initiative):
        self.army_idx = army_idx
        self.units = units
        self.hp = hp
        self.damage = damage
        self.attack = attack
        self.initiative = initiative
        self.weak = set()
        self.immune = set()

    def power(self):
        return max(self.units, 0) * self.damage

    def __repr__(self):
        return "Group" + repr(vars(self))


def part1(immunesys, infection):
    immunesys, infection = battle(immunesys, infection, 0)
    print("Part 1:")
    print("  ImmuneSys:", sum(g.units for g in immunesys))
    print("  Infection:", sum(g.units for g in infection))
    print()

def part2(immunesys, infection):
    lower, upper = 0, None
    immunesys_units_left = None
    while upper is None or upper - lower > 1:
        guess = max(2*lower, 1) if upper is None else (lower + upper) // 2
        won, units_left = immunesys_won(immunesys, infection, guess)
        if won:
            print(f"With boost {guess}, immune system won")
            upper = guess
            immunesys_units_left = units_left
        else:
            print(f"With boost {guess}, infection won")
            lower = guess
    print("Part 2 answer:", immunesys_units_left)

def immunesys_won(immunesys, infection, boost):
    immunesys, infection = battle(immunesys, infection, boost)
    return sum(g.units for g in infection) == 0, sum(g.units for g in immunesys)

def battle(immunesys, infection, boost):
    immunesys = copy.deepcopy(immunesys)
    infection = copy.deepcopy(infection)
    for group in immunesys:
        group.damage += boost
    done = False
    while not done and len(immunesys) > 0 and len(infection) > 0:
        done = fight(immunesys, infection)
        immunesys = prune(immunesys)
        infection = prune(infection)
    return immunesys, infection

def fight(army1, army2):
    armies = army1, army2
    hits = []
    enemies = set(army2), set(army1)
    for attacker in sorted(army1 + army2, key=targetsel_prio):
        enemy = enemies[attacker.army_idx]
        def attack_prio(t):
            return hitpoints(attacker, t), t.power(), t.initiative
        target = max(enemy, key=attack_prio, default=None)
        if target is not None and hitpoints(attacker, target) > 0:
            hits.append((attacker, target))
            enemy.remove(target)
    assert len(hits) > 0
    num_kills = 0
    for (attacker, target) in sorted(hits, key=hit_prio):
        kills = hitpoints(attacker, target) // target.hp
        target.units -= kills
        num_kills += kills
    return num_kills == 0

def hitpoints(attacker, target):
    if attacker.attack in target.immune:
        return 0
    if attacker.attack in target.weak:
        return attacker.power() * 2
    return attacker.power()

def targetsel_prio(group):
    return -group.power(), -group.initiative

def hit_prio(hit):
    attacker, target = hit
    return -attacker.initiative

def prune(army):
    return [ group for group in army if group.units > 0 ]


def main():
    inp = fileinput.input()

    assert next(inp).rstrip("\n") == "Immune System:"
    immunesys = parse_army(inp, 0)
    assert next(inp).rstrip("\n") == "Infection:"
    infection = parse_army(inp, 1)
    part1(immunesys, infection)
    part2(immunesys, infection)

def parse_army(inp, army_idx):
    army = []
    for line in inp:
        m = LINE_RE.match(line)
        if m is None:
            break
        group = Group(army_idx=army_idx, units=int(m.group(1)),
                      hp=int(m.group(2)), damage=int(m.group(4)),
                      attack=m.group(5), initiative=int(m.group(6)))
        modifiers = m.group(3)
        if modifiers is not None:
            for mod in modifiers.split("; "):
                ty, rest = mod.split(" to ")
                m = getattr(group, ty)
                m.update(rest.split(", "))
        army.append(group)
    return army

main()
