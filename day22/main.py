
#!/usr/bin/env python

import fileinput
import argparse
import re
import itertools

DEBUG = False


def main(files, part='1'):
    input_lines = [line.strip() for line in fileinput.input(files)]

    if part == '1':
        pass
    elif part == '2':
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default='1')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
