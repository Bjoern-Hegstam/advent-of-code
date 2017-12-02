def main():
    with open('input') as f:
        lines = f.readlines()
    rows = [[int(s) for s in line.split()] for line in lines]

    print('Answer part 1: {}'.format(calc_checksum(rows)))
    print('Answer part 1: {}'.format(sum_even_division(rows)))


def calc_checksum(rows):
    result = 0
    for row in rows:
        result += max(row) - min(row)
    return result


assert calc_checksum([[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8]]) == 18


def sum_even_division(rows):
    result = 0
    for row in rows:
        for i, x in enumerate(row[:-1]):
            for y in row[i + 1:]:
                if x % y == 0:
                    result += x // y
                elif y % x == 0:
                    result += y // x
    return result


assert sum_even_division([[5, 9, 2, 8], [9, 4, 7, 3], [3, 8, 6, 5]]) == 9

if __name__ == '__main__':
    main()
