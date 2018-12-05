alphabet = 'abcdefghijklmnopqrstuvwxyz'


def main():
    with open('input') as f:
        base_polymer = f.readline()

    reduced_polymer = react_polymer(base_polymer)

    print('Answer part 1: {}'.format(len(reduced_polymer)))

    reacted_lengths = {}
    for unit_pair in zip(alphabet, alphabet.upper()):
        print('Removing unit pair {}'.format(unit_pair))
        polymer = base_polymer.replace(unit_pair[0], '').replace(unit_pair[1], '')
        length = len(react_polymer(polymer))
        reacted_lengths[unit_pair] = length

        print('Removing unit pair {} gave length {}'.format(unit_pair, length))

    print('Answer part 2: {}'.format(min(reacted_lengths.values())))


def react_polymer(source_polymer):
    unit_pairs = list(zip(alphabet, alphabet.upper())) + list(zip(alphabet.upper(), alphabet))

    print('Reacting polymer')
    polymer = list(source_polymer)
    while True:
        polymer_reacted = False

        i = 0
        while i < len(polymer) - 1:
            if (polymer[i], polymer[i + 1]) in unit_pairs:
                del polymer[i:i+2]
                polymer_reacted = True
                continue
            else:
                i += 1

        if not polymer_reacted:
            return polymer


assert react_polymer('dabAcCaCBAcCcaDA') == list('dabCBAcaDA')


if __name__ == '__main__':
    main()
