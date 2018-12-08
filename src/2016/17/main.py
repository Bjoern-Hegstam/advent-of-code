#!/usr/bin/env python

import fileinput
import argparse
import hashlib

from collections import deque

DEBUG = False

class Node:
    def __init__(self, pos, path):
        self.pos = pos
        self.path = path

def main(files, part=1):
    input_lines = [line.strip() for line in fileinput.input(files)]

    passcode = input_lines[0]
    print('Passcode {}'.format(passcode))

    width = 4
    height = 4
    target_pos = (3, 3)

    queue = deque()
    queue.append(Node((0, 0), ''))

    target_paths = []

    while len(queue):
        if part == 1 and target_paths:
            break

        current = queue.popleft()

        for node in generate_neigbors(current, width, height, passcode):
            if DEBUG:
                print('Child: {}:{}'.format(node.path, node.pos))

            if node.pos == target_pos:
                target_paths.append(node)
            else:
                queue.append(node)

    if not target_paths:
        print('No path found')
        return

    if part == 1:
        print('Shortest path: {}'.format(target_paths[0].path))
    else:
        print('Longest path length: {}'.format(len(target_paths[-1].path)))


DIRECTIONS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}


def generate_neigbors(parent_node, width, height, passcode):
    door_states = hashlib.md5(bytes(passcode + parent_node.path, encoding='utf-8')).hexdigest()[:4]
    available_direction = [d for d, s in zip('UDLR', door_states) if s in 'bcdef']

    if DEBUG:
        print('\n{}:{} - {} {}'.format(parent_node.path, parent_node.pos, door_states, available_direction))

    for d, dpos in DIRECTIONS.items():
        if d not in available_direction:
            continue

        new_pos = (parent_node.pos[0] + dpos[0], parent_node.pos[1] + dpos[1])

        # Don't go outside of grid
        if new_pos[0] < 0 or \
            new_pos[0] == width or \
            new_pos[1] < 0 or \
            new_pos[1] == height:
            continue

        yield Node(new_pos, parent_node.path + d)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default=1)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
