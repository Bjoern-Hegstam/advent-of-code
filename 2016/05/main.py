#!/usr/bin/env python

import fileinput
import hashlib

door_id = fileinput.input()[0]
c = 0

password = ''

while True:

    hex_hash = hashlib.md5(bytes(door_id + str(c), encoding='utf-8')).hexdigest()
    if all(d == '0' for d in hex_hash[:5]):
        print(hex_hash)
        password += hex_hash[5]

    if len(password) == 8:
        break
    else:
        c += 1

print(password)