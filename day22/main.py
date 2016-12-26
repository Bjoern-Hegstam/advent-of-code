#!/usr/bin/env python

import fileinput
import argparse
import re

from heapq import heappop, heappush
from collections import namedtuple

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

def a_star_search(initial_state, h_fun, move_fun):
    # A* by Peter Norvig from https://nbviewer.jupyter.org/url/norvig.com/ipython/Advent%20of%20Code.ipynb
    frontier = [(h_fun(initial_state), initial_state)] # Priority queue of (f = g + h, State)
    previous = {initial_state: None} # From which state did we get to the state
    path_cost = {initial_state: 0} # Cost of best path to a state

    while frontier:
        (f, current_state) = heappop(frontier)

        if h_fun(current_state) == 0:
            return Path(previous, current_state)

        for neighbor in move_fun(current_state):
            new_cost = path_cost[current_state] + 1
            if neighbor not in path_cost or new_cost < path_cost[neighbor]:
                heappush(frontier, (new_cost + h_fun(neighbor), neighbor))
                path_cost[neighbor] = new_cost
                previous[neighbor] = current_state

    return dict(fail=True, front=len(frontier), prev=len(previous))


def Path(previous, s):
    "Return a list of states that lead to state s, according to the previous dict."
    return ([] if (s is None) else Path(previous, previous[s]) + [s])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default='1')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
