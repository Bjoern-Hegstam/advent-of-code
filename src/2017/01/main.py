def main():
    with open('input') as f:
        line = f.readline()
    print('Answer part 1: {}'.format(calc_captcha(line, 1)))
    print('Answer part 2: {}'.format(calc_captcha(line, len(line) // 2)))


def calc_captcha(line, idx_step):
    return sum([int(num) for idx, num in enumerate(line) if line[idx] == line[(idx + idx_step) % len(line)]])


assert calc_captcha('1122', 1) == 3
assert calc_captcha('1111', 1) == 4
assert calc_captcha('1234', 1) == 0
assert calc_captcha('91212129', 1) == 9

assert calc_captcha('1212', 2) == 6
assert calc_captcha('1221', 2) == 0
assert calc_captcha('123425', 3) == 4
assert calc_captcha('123123', 3) == 12
assert calc_captcha('12131415', 4) == 4

if __name__ == '__main__':
    main()
