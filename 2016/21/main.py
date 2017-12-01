#!/usr/bin/env python

import fileinput
import argparse
import re
import itertools

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
        self.pattern = re.compile(r'^swap letter (?P<cx>\w) with letter (?P<cy>\w)$')

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
        self.pattern = re.compile(r'^rotate (?P<dir>left|right) (?P<num_steps>\d+) steps?$')

    def run(self, match, password):
        direction = 1 if match.group('dir') == 'left' else -1
        num_steps = int(match.group('num_steps'))

        move = direction*num_steps % len(password)

        return password[move:] + password[:move]

class RotateBasedOnLetterPosition:
    def __init__(self):
        self.pattern = re.compile(r'^rotate based on position of letter (?P<cx>\w)$')

    def run(self, match, password):
        cx = match.group('cx')
        idx = password.index(cx)

        # Always rotate to the right => move < 0
        move = -1 - idx - (1 if idx >= 4 else 0)
        move %= len(password)

        return password[move:] + password[:move]

class ReverseInterval:
    def __init__(self):
        self.pattern = re.compile(r'^reverse positions (?P<x>\d+) through (?P<y>\d+)$')

    def run(self, match, password):
        x = int(match.group('x'))
        y = int(match.group('y'))

        return password[:x] + list(reversed(password[x:y+1])) + password[y+1:]


class MoveLetter:
    def __init__(self):
        self.pattern = re.compile(r'^move position (?P<x>\d+) to position (?P<y>\d+)$')

    def run(self, match, password):
        x = int(match.group('x'))
        y = int(match.group('y'))

        if x < y:
            return password[:x] + password[x+1:y+1] + [password[x]] + password[y+1:]
        else:
            return password[:y] + [password[x]] + password[y:x] + password[x+1:]


OPERATIONS = [
        SwapPositions(),
        SwapLetters(),
        RotateFixedDirection(),
        RotateBasedOnLetterPosition(),
        ReverseInterval(),
        MoveLetter()
    ]


def main(files, part='1'):
    instructions = [line.strip() for line in fileinput.input(files)]

    if part == '1':
        print(scramble_password('abcdefgh', instructions))
    elif part == '2':
        for pwd in itertools.permutations(list('abcdefgh'), 8):
            scramled = scramble_password(pwd, instructions)
            if scramled == 'fbgdceah':
                print(''.join(pwd))
                return


def scramble_password(password, instructions):
    if isinstance(password, str) or isinstance(password, tuple):
        scrambled_pass = list(password)
    else:
        assert isinstance(password, list)
        scrambled_pass = password

    for line in instructions:
        if DEBUG:
            print(line)
        for op in OPERATIONS:
            match = op.pattern.match(line)
            if match:
                scrambled_pass = op.run(match, scrambled_pass)
                if DEBUG:
                    print(''.join(scrambled_pass))
                    print()
                break

    return ''.join(scrambled_pass)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default='1')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
