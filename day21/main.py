#!/usr/bin/env python

import fileinput
import argparse
import re

DEBUG = False

class SwapOperation:
    def __init__(self):
        self.pattern = re.compile(r'^swap position (?P<x>\d+) with position (?P<y>\d+)$')

    def run(self, match, password):
        x = int(match.group('x'))
        y = int(match.group('y'))
        password[x], password[y] = password[y], password[x]        



def main(files, part='1'):
    operations = [
        SwapOperation()
    ]

    password = list('abcde')

    for line in fileinput.input(files):
        for op in operations:
            match = op.pattern.match(line)
            if match:
                op.run(match, password)
                break


    print(''.join(password))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default='1')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
