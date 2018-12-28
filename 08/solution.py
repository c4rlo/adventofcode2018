#!/usr/bin/python

license = list(map(int, open('input').read().split()))

class Node:
    def __init__(self):
        self.children = []
        self.entries = []

def read_node(data):
    node = Node()
    num_children = data[0]
    num_entries = data[1]
    i = 2
    for _ in range(num_children):
        child, child_len = read_node(data[i:])
        node.children.append(child)
        i += child_len
    node.entries = data[i:i+num_entries]
    return node, i+num_entries

root, root_len = read_node(license)
assert root_len == len(license)

def entries_total(node):
    return sum(node.entries) + sum(entries_total(c) for c in node.children)

print("Part 1 answer:", entries_total(root))

def value(node):
    if len(node.children) == 0:
        return sum(node.entries)
    else:
        return sum(value(node.children[i-1]) for i in node.entries
                   if i <= len(node.children))

print("Part 2 answer:", value(root))
