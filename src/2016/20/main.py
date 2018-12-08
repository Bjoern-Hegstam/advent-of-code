#!/usr/bin/env python

import fileinput
import argparse

DEBUG = False

def main(files, part='1'):
    not_allowed_nums = {}
    intervals = sorted([list(map(int, line.split('-'))) for line in fileinput.input(files)], key=lambda i: i[0])
    merged_intervals = []

    current = intervals[0].copy()
    for interval in intervals[1:]:
        if current[1] + 1 <  interval[0]:
            merged_intervals.append(current)
            current = interval.copy()
        elif current[1] + 1 == interval[0] or current[1] < interval[1]:
            current[1] = interval[1]
    merged_intervals.append(current)

    if part == '1':
        solve_part_one(merged_intervals)
    else:
        solve_part_two(merged_intervals)


def solve_part_one(non_overlapping_intervals):
    lowest_ip = 0
    for interval in non_overlapping_intervals:
        if lowest_ip >= interval[0] and lowest_ip <= interval[1]:
            lowest_ip = interval[1] + 1
    print(lowest_ip)


def solve_part_two(non_overlapping_intervals):
    not_allowed_count = 0

    for interval in non_overlapping_intervals:
        not_allowed_count += interval[1] - interval[0] + 1

    print(4294967295 + 1 - not_allowed_count)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default='1')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug

    main(args.files, part=args.part)
