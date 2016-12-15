#!/usr/bin/env python

import fileinput
import argparse
import re

class Disc:
    def __init__(self, h, p0, N):
        self.h = h
        self.p0 = p0
        self.N = N

def main(part, files):
    '''
    t = time
    h = disc height/number
    N = Number of positions
    p0 = Initial position

    pos(t) = h + p0 + t (mod N)

    Ball can pass at time t if pos(t) = 0

    0 = 1 + 4 + t + 5*a
    0 = 2 + 1 + t + 2*b

    =>

    0 = 5 + t + 5*a
    0 = 3 + t + 2*b

    0 | 5 5 0
    0 | 3 0 2
    '''

    discs = []
    lines = [line.strip() for line in fileinput.input(files)]

    for line in lines:
        vals = re.match(r'^Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.$', line)
        params = [int(v) for v in vals.groups()]
        discs.append(Disc(params[0], params[2], params[1]))
        
    # Print equation system
    variables = 'abcdefghijklmnopqrstuvxyz'
    for disc in discs:
        print('0 = ', end='')
        print('{:2d}'.format(disc.h + disc.p0), end='')
        print('+ t + {0:2d}{1}'.format(disc.N, variables[disc.h - 1]), end=', ')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', default='1', type=int)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.part, args.files)
