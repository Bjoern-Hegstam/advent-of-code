from collections import deque

from util.constants import ALPHABET_LOWER, ALPHABET_UPPER

unit_pairs = list(zip(ALPHABET_LOWER, ALPHABET_UPPER)) + list(zip(ALPHABET_UPPER, ALPHABET_LOWER))


def main():
    with open('input') as f:
        base_polymer = f.readline()

    reduced_polymer = react_polymer(base_polymer)

    print('Answer part 1: {}'.format(len(reduced_polymer)))

    reacted_lengths = {}
    for unit_pair in zip(ALPHABET_LOWER, ALPHABET_UPPER):
        reacted_lengths[unit_pair] = len(react_polymer(base_polymer, excluded_unit_pair=unit_pair))

    print('Answer part 2: {}'.format(min(reacted_lengths.values())))


def react_polymer(source_polymer, excluded_unit_pair=None):
    polymer = deque()
    for unit in source_polymer:
        if excluded_unit_pair and (unit == excluded_unit_pair[0] or unit == excluded_unit_pair[1]):
            continue
        elif not polymer:
            polymer.append(unit)
        elif (polymer[-1], unit) in unit_pairs:
            polymer.pop()
        else:
            polymer.append(unit)

    return list(polymer)


assert react_polymer('dabAcCaCBAcCcaDA') == list('dabCBAcaDA')


if __name__ == '__main__':
    main()
