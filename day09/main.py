#!/usr/bin/env python

import fileinput
import argparse

def compute_decompressed_length(data, recursive):
    if not data:
        return 0

    if data[0] == '(':
        # Convert '(AxB)' to [A, B]
        spec_end_idx = data.find(')')
        size_spec = data[1:spec_end_idx].split('x')
        length = int(size_spec[0])
        count = int(size_spec[1])

        sub_data = data[spec_end_idx+1:spec_end_idx+length+1]
        if '(' in sub_data and recursive:
            data_length = compute_decompressed_length(sub_data, recursive)
        else:
            data_length = len(sub_data)

        return count * data_length + compute_decompressed_length(data[spec_end_idx+length+1:], recursive)

    if not '(' in data:
        return len(data)

    # Data is of the form X+(AxB)+X+. Find length of part before marker and decompress the rest
    uncompressed_length = data.find('(')
    return uncompressed_length + compute_decompressed_length(data[uncompressed_length:], recursive)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', default='1', type=int)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    for line in fileinput.input(args.files):
        print(compute_decompressed_length(line.strip(), recursive=(args.part == 2)))
