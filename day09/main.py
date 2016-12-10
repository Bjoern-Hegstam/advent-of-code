#!/usr/bin/env python

import fileinput

DEBUG = False

if __name__ == '__main__':
    total_length = 0
    data = fileinput.input()[0].strip()

    i = 0
    while i < len(data):
        if data[i] == '(':
            # Convert '(AxB)' to [A, B]
            spec_end_idx = data.find(')', i)
            spec_str_length = spec_end_idx - i + 1
            size_spec = data[i+1:spec_end_idx].split('x')
            length = int(size_spec[0])
            count = int(size_spec[1])

            if DEBUG:
                print(data[spec_end_idx+1:spec_end_idx+length+1]*count, end="")

            total_length += length * count
            i += spec_str_length + length
        else:
            if DEBUG:
                print(data[i], end="")

            total_length += 1
            i += 1

    print()
    print(total_length)
