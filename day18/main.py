#!/usr/bin/env python

import fileinput
import argparse

class Tile:
    SAFE = '.'
    TRAP = '^'

TRAP_PATTERNS = set()
TRAP_PATTERNS.add(Tile.TRAP + Tile.SAFE + Tile.SAFE)
TRAP_PATTERNS.add(Tile.TRAP + Tile.TRAP + Tile.SAFE)
TRAP_PATTERNS.add(Tile.SAFE + Tile.TRAP + Tile.TRAP)
TRAP_PATTERNS.add(Tile.SAFE + Tile.SAFE + Tile.TRAP)

class Line:
    def __init__(self, data):
        self.__data = data
        self.safe_count = len([c for c in data if c == Tile.SAFE]) - 2

    @staticmethod
    def create_from_string(str_data):
        return Line('{0}{1}{0}'.format(Tile.SAFE, str_data))

    @staticmethod
    def create_from_previous(prev_line):
        data = [Tile.SAFE]
        for idx in range(len(prev_line.__data[1:-1])):
            if prev_line.__data[idx:idx+3] in TRAP_PATTERNS:
                data.append(Tile.TRAP)
            else:
                data.append(Tile.SAFE)
        data.append(Tile.SAFE)
        return Line(''.join(data))


    def __repr__(self):
        return ''.join(self.__data)


def main(files):
    input_lines = [line.strip() for line in fileinput.input(files)]
    target_length = int(input_lines[1])

    current = Line.create_from_string(input_lines[0])
    safe_count = current.safe_count
    for i in range(target_length - 1):
        current = Line.create_from_previous(current)
        safe_count += current.safe_count

        if i % 20000 == 0:
            print('{0}: {1}'.format(i, safe_count), flush=True)
    
    print('{0}: {1}'.format(target_length, safe_count), flush=True)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.files)
