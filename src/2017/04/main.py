def main():
    with open('input') as f:
        lines = f.readlines()

    print('Answer part 1: {}'.format(solve_part_one(lines)))
    print('Answer part 2: {}'.format(solve_part_two(lines)))


def solve_part_one(lines):
    return len([line for line in lines if is_valid(line)])


def solve_part_two(lines):
    return len([line for line in lines if is_valid(line, sort_letters=True)])


def is_valid(passphrase, sort_letters=False):
    words = passphrase.split()
    d = set()
    for word in words:

        if sort_letters:
            letters = list(word)
            letters.sort()
            key = ''.join(letters)
        else:
            key = word

        if key in d:
            return False
        else:
            d.add(key)
    return True


if __name__ == '__main__':
    main()
