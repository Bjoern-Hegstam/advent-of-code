#!/usr/bin/env python

import fileinput
import argparse
import re

DEBUG = False

class SwapPositions:
    def __init__(self):
        self.pattern = re.compile(r'^swap position (?P<x>\d+) with position (?P<y>\d+)$')

    def run(self, match, password):
        x = int(match.group('x'))
        y = int(match.group('y'))

        new_pass = password.copy()
        new_pass[x], new_pass[y] = password[y], password[x]
        return new_pass

class SwapLetters:
    def __init__(self):
        self.pattern = re.compile(r'swap letter (?P<cx>\w) with letter (?P<cy>\w)$')

    def run(self, match, password):
        cx = match.group('cx')
        cy = match.group('cy')

        x = password.index(cx)
        y = password.index(cy)

        new_pass = password.copy()
        new_pass[x], new_pass[y] = password[y], password[x]
        return new_pass

class RotateFixedDirection:
    def __init__(self):
        self.pattern = re.compile(r'rotate (?P<dir>left|right) (?P<num_steps>\d+) steps?$')

    def run(self, match, password):
        print('Match')
        direction = 1 if match.group('dir') == 'left' else -1
        num_steps = int(match.group('num_steps'))

        move = direction*num_steps % len(password)
        print(move)

        new_pass = password[move:] + password[:move]
        return new_pass


def main(files, part='1'):
    operations = [
        SwapPositions(),
        SwapLetters(),
        RotateFixedDirection()
    ]

    password = list('abcde')

    for line in fileinput.input(files):
        for op in operations:
            match = op.pattern.match(line)
            if match:
                password = op.run(match, password)
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
