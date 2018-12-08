#!/usr/bin/env python

import fileinput


valid_count = 0

val_buffer = []

def is_valid_triangle(a, b, c):
    return a + b > c and b + c > a and c + a > b

for line in fileinput.input():
    val_buffer.append([int(val) for val in line.split()])

    if len(val_buffer) < 3:
        continue

    for i in range(3):
        if is_valid_triangle(val_buffer[0][i], val_buffer[1][i], val_buffer[2][i]):
            valid_count += 1

    val_buffer = []


print(valid_count)