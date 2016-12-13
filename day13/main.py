#!/usr/bin/env python

import fileinput
import argparse

class Tile:
    WALL = '#'
    OPEN = '.'


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


def draw_map(m, top_left, bottom_right):
    print('  ' + ''.join([str(x) for x in range(top_left[0], bottom_right[0])]))
    
    for y in range(top_left[1], bottom_right[1]):
        print('%s ' % y, end='')
        for x in range(top_left[0], bottom_right[0]):
            print(m.get((x, y)), end='')
        print()


def main(part, files):
    lines = [line.strip() for line in fileinput.input(files)]
    seed = int(lines[0])
    target = tuple([int(d) for d in lines[1].split(',')])

    m = Map(seed)

    draw_map(m, (0, 0), (10, 7))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', default='1', type=int)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.part, args.files)
