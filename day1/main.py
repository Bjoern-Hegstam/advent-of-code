#!/usr/bin/env python

import fileinput

visited_locations = {(0, 0)}

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

        for step in range(magnitude):
            pos_x += dir_x
            pos_y += dir_y

            if (pos_x, pos_y) in visited_locations:
                print('Location visited twice: (%s, %s)' % (pos_x, pos_y))
            else:
                visited_locations.add((pos_x, pos_y))

    print(pos_x + pos_y)
