#!/usr/bin/env python

import fileinput
import argparse
import hashlib

class Hash:
    def __init__(self, seed, idx):
        self.hash = hashlib.md5(bytes(seed + str(idx), encoding='utf-8')).hexdigest()

        char_counts = []
        current = self.hash[0]
        count = 1
        for c in self.hash[1:]:
            if c != current:
                char_counts.append((c, count))
                current = 1
                count = 1
            else:
                count += 1

        self.triplet_char = None
        for c, count in char_counts:
            if count >= 3:
                self.triplet_char = c
                break

        self.seven_series_keys = set(c for c, count in char_counts if count >= 7)

    def __repr__(self):
        return self.hash


def main(part, files):
    lines = [line.strip() for line in fileinput.input(files)]
    seed = lines[0]

    print(Hash(seed, 18))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', default='1', type=int)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.part, args.files)
