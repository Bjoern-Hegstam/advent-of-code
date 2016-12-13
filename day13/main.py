#!/usr/bin/env python

import fileinput
import argparse

def main(part, files):
    lines = [line.strip() for line in fileinput.input(files)]
    seed = int(lines[0])
    start = tuple([int(d) for d in lines[1].split(',')])
    target = tuple([int(d) for d in lines[2].split(',')])

    m = Map(seed)
    m.draw((0, 0), (10, 10))
    return

    path = find_path(m, start, target)
    print('Path length: %s' % len(path))


def find_path(m, start, target):
    closed_set = set()
    open_set = set()

    # Maps position to its previous position
    came_from = {}

    g_score = {}
    f_score = {}



    return []


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
