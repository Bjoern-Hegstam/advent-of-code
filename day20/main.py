#!/usr/bin/env python

import fileinput
import argparse

DEBUG = False

def main(files, part=1):
    not_allowed_nums = {}
    intervals = sorted([tuple(map(int, line.split('-'))) for line in fileinput.input(files)], key=lambda i: i[0])
    
    lowest_ip = 0
    for interval in intervals:
        if lowest_ip >= interval[0] and lowest_ip <= interval[1]:
            lowest_ip = interval[1] + 1

    print(lowest_ip)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default=1)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
