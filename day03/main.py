#!/usr/bin/env python

import fileinput


valid_count = 0

for line in fileinput.input():
    vals = [int(val) for val in line.split()]
    if vals[0] + vals[1] > vals[2] and vals[1] + vals[2] > vals[0] and vals[2] + vals[0] > vals[1]:
       valid_count += 1

print(valid_count)