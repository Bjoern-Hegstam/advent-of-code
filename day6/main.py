#!/usr/bin/env python

import fileinput

histograms = [{} for x in range(8)]

for line in fileinput.input():
    for idx, letter in enumerate(line.strip()):
        h = histograms[idx]
        h[letter] = 1 + h.get(letter, 0)


print(''.join([max(h.keys(), key=h.get) for h in histograms]))
