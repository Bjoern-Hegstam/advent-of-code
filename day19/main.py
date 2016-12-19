#!/usr/bin/env python

import fileinput
import argparse

def main(files):
    input_lines = [line.strip() for line in fileinput.input(files)]
    N = int(input_lines[0])

    # 1 2 3 4 5 6 | N = 6, idx(n) = n 
    # 1   3   5   | N = 3, idx(n) = 1 + 2*n = 1 + 2*idx'(n)
    #         5   | N = 1

    # 1 2 3 4 5 6 7 8 9 10 | N = 10, n_0 = 1, dn = 1
    # 1   3   5   7   9    | N = 5, n_0 = 1, dn = 2
    #         5       9    | N = 2, n_0 = 5, dn = 4
    #         5            | N = 1, n_0 = 1

    n_0 = 1
    dn = 1
    while N > 1:
        dn *= 2
        if N % 2 != 0:
            n_0 += dn
            N = (N - 1)/ 2
        else:
            N /= 2


    print(n_0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.files)
