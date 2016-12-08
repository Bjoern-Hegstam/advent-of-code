#!/usr/bin/env python

import fileinput

sector_id_sum = 0

for line in fileinput.input():
    histogram = {}

    for letter in line[:line.rfind('-')]:
        if letter == '-':
            continue

        histogram[letter] = 1 + histogram.get(letter, 0)

    sector_id = line.split('-')[-1].split('[')[0]
    room_hash = line.split('-')[-1].split('[')[1][:-2]

    # Sort is stable. Sort by letter, then by count desc.
    expected_hash = ''.join(letter for letter in sorted(sorted(histogram), key=histogram.get, reverse=True)[0:5])    

    #print(histogram)
    #print(sector_id)
    #print(room_hash)
    #print(expected_hash)

    if expected_hash == room_hash:
        sector_id_sum += int(sector_id)

print(sector_id_sum)