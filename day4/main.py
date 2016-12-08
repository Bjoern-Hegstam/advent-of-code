#!/usr/bin/env python

import fileinput

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
sector_id_sum = 0

for line in fileinput.input():
    histogram = {}
    encrypted_name = line[:line.rfind('-')]

    for letter in encrypted_name:
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

    if expected_hash != room_hash:
        continue

    sector_id_sum += int(sector_id)

    decrypted_name = ''
    for letter in encrypted_name:
        if letter == '-':
            decrypted_name += ' '
            continue

        decrypted_name += ALPHABET[(ALPHABET.index(letter) + int(sector_id)) % len(ALPHABET)]

    # Filter out all names with easter related words in them. (Instead of guessing the correct name)
    banned_words = [
        'egg',
        'basket',
        'flower',
        'bunny',
        'rabbit',
        'scavenger',
        'jellybean',
        'candy',
        'dye',
        'chocolate',
        'grass'
    ]

    if all(word not in decrypted_name for word in banned_words):
        print('%s - %s' % (sector_id, decrypted_name))

print(sector_id_sum)
