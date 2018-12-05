alphabet = 'abcdefghijklmnopqrstuvwxyz'


def main():
    with open('input') as f:
        base_line = f.readline()

    reduced_polymer = reduce_polymer(base_line)

    print('Answer part 1: {}'.format(len(reduced_polymer)))


def reduce_polymer(base_line):
    unit_pairs = list(zip(alphabet, alphabet.upper())) + list(zip(alphabet.upper(), alphabet))

    line = base_line
    while True:
        new_line = ''

        i = 0
        while i < len(line) - 1:
            if (line[i], line[i + 1]) in unit_pairs:
                i += 2
                continue

            new_line += line[i]
            i += 1

        if i == len(line) - 1:
            new_line += line[-1]

        if new_line != line:
            line = new_line
        else:
            return new_line


assert reduce_polymer('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'


if __name__ == '__main__':
    main()
