#!/usr/bin/env python

import fileinput

for line in fileinput.input():
    pos_x = 0
    pos_y = 0

    dir_x = 0
    dir_y = 1

    for (rotation, magnitude) in [(s[0:1], int(s[1:])) for s in line.split(', ')]:
        if rotation == 'L':
            dir_x, dir_y = -dir_y, dir_x
        else:
            dir_x, dir_y = dir_y, -dir_x

        pos_x += magnitude * dir_x
        pos_y += magnitude * dir_y

    print(pos_x + pos_y)