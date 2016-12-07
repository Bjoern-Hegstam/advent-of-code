#!/usr/bin/env python

import fileinput

x = 0
y = 0

KEYPAD = {
    1: {-1: 1, 0: 2, 1: 3},
    0: {-1: 4, 0: 5, 1: 6},
    -1: {-1: 7, 0: 8, 1: 9}
}

code = ''

for line in fileinput.input():
    for direction in line:
        if direction == 'U' and y < 1:
            y += 1
        elif direction == 'D' and y > -1:
            y -= 1
        elif direction == 'L' and x > -1:
            x -= 1
        elif direction == 'R' and x < 1:
            x += 1

    code += str(KEYPAD[y][x])

print(code)