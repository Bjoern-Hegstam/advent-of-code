#!/usr/bin/env python

import fileinput
import argparse
import re

from collections import namedtuple

from util.path import a_star_search

DEBUG = False


Node = namedtuple('Node', 'x, y, size, used, avail, use')

def main(files, part='1'):
    node_pattern = re.compile(r'^/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+(?P<use>\d+)%$')

    nodes = []

    for line in fileinput.input(files):
        match = node_pattern.match(line)
        if not match:
            continue

        nodes.append(Node(
                int(match.group('x')),
                int(match.group('y')),
                int(match.group('size')),
                int(match.group('used')),
                int(match.group('avail')),
                int(match.group('used'))
            ))

    if part == '1':
        find_num_viable_pairs(nodes)
    elif part == '2':
        solve_part_two(nodes)


def find_num_viable_pairs(nodes):
    count = 0
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2 and 0 < n1.used <= n2.avail:
                count += 1

    print(count)


State = namedtuple('State', 'empty_pos, data_pos')

def solve_part_two(nodes):
    max_x = max(node.x for node in nodes)
    max_y = max(node.y for node in nodes)

    empty_node = min(nodes, key=lambda n: n.used)
    empty_pos = (empty_node.x, empty_node.y)

    print('Max x: {}'.format(max_x))
    print('Max y: {}'.format(max_y))
    print('Empty node: {}'.format(empty_pos))

    initial_state = State(empty_pos, (max_x, 0))
    h_fun = lambda s: s.data_pos[0] + s.data_pos[1]
    move_fun = lambda s: next_states(nodes, s)

    res = a_star_search(initial_state, h_fun, move_fun)

    print('Num steps required: {}'.format(len(res) - 1))

def next_states(nodes, state):
    grid = {(n.x, n.y): n for n in nodes}

    for neighbor_pos in neighbors4(state.empty_pos):
        if neighbor_pos not in grid:
            continue

        neighbor = grid[neighbor_pos]
        empty_node = grid[state.empty_pos]

        if neighbor.used < empty_node.size:
            new_data_pos = (state.empty_pos if neighbor_pos == state.data_pos else state.data_pos)
            yield State(neighbor_pos, new_data_pos)


def neighbors4(pos):
    x, y = pos
    return [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y)
    ]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default='1')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
