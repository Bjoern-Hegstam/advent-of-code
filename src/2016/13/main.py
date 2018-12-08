#!/usr/bin/env python

import fileinput
import argparse
import math

def main(part, files):
    lines = [line.strip() for line in fileinput.input(files)]
    seed = int(lines[0])
    m = Map(seed)
    start = tuple([int(d) for d in lines[1].split(',')])

    if part == 1:
        target = tuple([int(d) for d in lines[2].split(',')])

        path = find_path(m, start, target)

        print('Step count: %s' % (len(path) - 1))
    else:
        path_count = 0

        for y in range(52):
            for x in range(52):
                target = (x, y)

                if m.get(target) == Tile.WALL:
                    continue

                # Search from target to start in case target in inaccessible from start
                path = find_path(m, target, start)
                step_count = len(path) - 1
                if path and step_count <= 50:
                    path_count += 1

        print('Num targets reachable in 50 steps or less: %s' % path_count)


def find_path(m, start, target):
    '''
    A* implemented from pseducode @ https://en.wikipedia.org/wiki/A*_search_algorithm (2016-12-13)
    '''
    closed_set = set()
    open_set = set()

    dist = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    h = lambda pos: dist(pos, target)

    # Maps position to its previous position
    came_from = {}

    g_score = {}
    f_score = {}

    g_score[start] = 0
    f_score[start] = h(start)

    open_set.add(start)

    while open_set:
        current = min([(p, f_score.get(p, math.inf)) for p in open_set], key=lambda d: d[1])[0]
        if current == target:
            return build_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in generate_neighbors(m, current):
            if neighbor in closed_set:
                continue

            g = g_score[current] + dist(current, neighbor)
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif g >= g_score.get(neighbor, math.inf):
                # Already now of a better path to this position
                continue

            # Best path here so far
            came_from[neighbor] = current
            g_score[neighbor] = g
            f_score[neighbor] = g_score[neighbor] + h(neighbor)

    return []


def generate_neighbors(m, pos):
    for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        new_pos = (pos[0] + dx, pos[1] + dy)

        if new_pos[0] < 0 or new_pos[1] < 0:
            continue

        if m.get(new_pos) == Tile.OPEN:
            yield new_pos


def build_path(came_from, end_pos):
    path = [end_pos]
    temp = end_pos
    while temp in came_from:
        temp = came_from[temp]
        path.append(temp)
    return path


class Tile:
    WALL = '#'
    OPEN = '.'
    PATH = 'O'


class Map:
    def __init__(self, seed):
        self.__seed = seed
        self.__map = {}

    def get(self, pos):
        if pos not in self.__map:
            self.__map[pos] = self.__calculate_map_value(pos)

        return self.__map[pos]

    def __calculate_map_value(self, pos):
        x = pos[0]
        y = pos[1]

        val = x*x + 3*x + 2*x*y + y + y*y
        val += self.__seed
        count_ones = len([d for d in bin(val) if d == '1'])

        return Tile.OPEN if count_ones % 2 == 0 else Tile.WALL

    def draw(self, top_left, bottom_right, path=None):
        if not path:
            path = []

        print('  ' + ''.join([str(x) for x in range(top_left[0], bottom_right[0])]))

        for y in range(top_left[1], bottom_right[1]):
            print('%s ' % y, end='')
            for x in range(top_left[0], bottom_right[0]):
                print(Tile.PATH if (x, y) in path else self.get((x, y)), end='')
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', default='1', type=int)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.part, args.files)
