#!/usr/bin/env python

import fileinput
import argparse

def main(files, simulate=False, debug=False):
    discs = []
    lines = [line.strip() for line in fileinput.input(files)]

    initial_state = lines[0]
    target_length = int(lines[1])

    data = generate_data(initial_state, target_length)
    checksum = calculate_checksum(data[:target_length])

    print(checksum)


def generate_data(initial_state, target_length):
    data = initial_state
    flip_bit = lambda b: '1' if b == '0' else '0'

    while len(data) < target_length:
        data += '0' + ''.join(flip_bit(b) for b in reversed(data))

    return data


def calculate_checksum(data):
    f = lambda val: ''.join(('1' if b1 == b2 else '0') for b1, b2 in zip(val[:-1:2], val[1::2]))

    checksum = data
    while len(checksum) % 2 == 0:
        checksum = f(checksum)

    return checksum



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.files)
