#!/usr/bin/env python

import fileinput

x = 0
y = 0

SQUARE_KEYPAD = {
    (1, -1): '1',
    (1, 0): '2',
    (1, 1): '3',

    (0, -1): '4',
    (0, 0): '5',
    (0, 1): '6',

    (-1, -1): '7',
    (-1, 0): '8',
    (-1, 1): '9',
}

STAR_KEYPAD = {
    (2, 0): '1',

    (1, -1): '2',
    (1, 0): '3',
    (1, 1): '4',

    (0, -2): '5',
    (0, -1): '6',
    (0, 0): '7',
    (0, 1): '8',
    (0, 2): '9',

    (-1, -1): 'A',
    (-1, 0): 'B',
    (-1, 1): 'C',

    (-2, 0): 'D'
}

code = ''

#keypad = SQUARE_KEYPAD
keypad = STAR_KEYPAD

for line in fileinput.input():
    for direction in line:
        if direction == 'U' and (y + 1, x) in keypad:
            y += 1
        elif direction == 'D' and (y - 1, x) in keypad:
            y -= 1
        elif direction == 'L' and (y, x - 1) in keypad:
            x -= 1
        elif direction == 'R' and (y, x + 1) in keypad:
            x += 1

    code += keypad[(y,x)]

print(code)