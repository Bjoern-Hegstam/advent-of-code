#!/usr/bin/env python

import fileinput
import hashlib
import sys

door_id = fileinput.input()[0]
c = 0

password = ['_'] * 8

while True:
    sys.stdout.flush()
    hex_hash = hashlib.md5(bytes(door_id + str(c), encoding='utf-8')).hexdigest()
    c += 1

    if all(d == '0' for d in hex_hash[:5]):
        if not hex_hash[5] in '01234567':
            print('%s - Rejected: Invalid position' % hex_hash)
            continue

        pos = int(hex_hash[5])
        if password[pos] != '_':
            print('%s - Rejected: Position filled' % hex_hash)
            continue

        print('%s - Accepted: (%s, %s)' % (hex_hash, pos, hex_hash[6]))
        password[pos] = hex_hash[6]

        print(password)

    if all(c != '_' for c in password):
        break

print(''.join(password))
