#!/usr/bin/env python

import fileinput
import argparse
import re

DEBUG = False


class Node:
    def __init__(self, x, y, size, used, avail, use):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.avail = avail
        self.use = use


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
        print(find_num_viable_pairs(nodes))


def find_num_viable_pairs(nodes):
    count = 0
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2 and 0 < n1.used <= n2.avail:
                count += 1

    return count




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default='1')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
