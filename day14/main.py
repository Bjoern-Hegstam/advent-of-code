#!/usr/bin/env python

import fileinput
import argparse
import hashlib

class Hash:
    def __init__(self, seed, idx, stretched=False):
        self.hash = self.__generate_hash(seed, idx, 2016 if stretched else 0)

        char_counts = []
        current_char = self.hash[0]
        count = 1
        for c in self.hash[1:]:
            if c != current_char:
                char_counts.append((current_char, count))
                current_char = c
                count = 1
            else:
                count += 1
        char_counts.append((current_char, count))

        self.triplet_char = None
        for c, count in char_counts:
            if count >= 3:
                self.triplet_char = c
                break

        self.seven_series_keys = set(c for c, count in char_counts if count >= 5)

    @staticmethod
    def __generate_hash(seed, idx, iterations):
        hash_fun = lambda value: hashlib.md5(bytes(value, encoding='utf-8')).hexdigest()
        tmp = hash_fun(seed + str(idx))
        for i in range(iterations):
            tmp = hash_fun(tmp)
        return tmp

    def __repr__(self):
        return self.hash


class HashCache:
    def __init__(self, seed, stretched=False):
        self.__seed = seed
        self.__cache = {}
        self.__stretched = stretched

    def get(self, idx):
        if idx not in self.__cache:
            self.__cache[idx] = Hash(self.__seed, idx, stretched=self.__stretched)

        return self.__cache[idx]

    def remove(self, idx):
        del self.__cache[idx]


def main(part, files):
    lines = [line.strip() for line in fileinput.input(files)]
    seed = lines[0]

    pad_keys = find_pad_keys(seed, HashCache(seed, stretched=(args.part == 2)))
    print(pad_keys)


def find_pad_keys(seed, hash_cache):
    pad_keys = []

    idx = 0
    while len(pad_keys) < 64:
        if is_valid_hash_key(hash_cache, idx):
            pad_keys.append((idx, hash_cache.get(idx)))
            print_pad_key_progress(idx, pad_keys)

        if idx % 500 == 0:
            print_pad_key_progress(idx, pad_keys)

        # Prevent cache from growing too much
        hash_cache.remove(idx)
        idx += 1

    return pad_keys


def is_valid_hash_key(hash_cache, idx):
    potential_key = hash_cache.get(idx)
    if not potential_key.triplet_char:
        return False

    for d_idx in range(1, 1001):
        if potential_key.triplet_char in hash_cache.get(idx + d_idx).seven_series_keys:
            return True

    return False


def print_pad_key_progress(idx, pad_keys):
    print('%s - %s' % (idx, len(pad_keys)), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', default='1', type=int)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.part, args.files)
