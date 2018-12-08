def main():
    with open('input') as f:
        lines = f.readlines()

    frequency_changes = [int(v) for v in lines]

    print('Answer part 1: {}'.format(sum(frequency_changes)))
    print('Answer part 2: {}'.format(find_first_repeated_frequency(frequency_changes)))


def find_first_repeated_frequency(frequency_changes):
    seen_frequencies = set()
    seen_frequencies.add(0)

    f = 0
    while True:
        for df in frequency_changes:
            f = f + df
            if f in seen_frequencies:
                return f
            seen_frequencies.add(f)


if __name__ == '__main__':
    main()
