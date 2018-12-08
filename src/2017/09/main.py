def main():
    with open('input') as f:
        data = f.readline()

    score, garbage_count = analyze(data)
    print('Answer part 1: {}'.format(score))
    print('Answer part 2: {}'.format(garbage_count))


def analyze(data):
    idx = 0
    depth = 0
    total_score = 0
    non_cancelled_garbage_count = 0
    in_garbage = False

    while idx < len(data):
        c = data[idx]
        if in_garbage:
            if c == '>':
                in_garbage = False
                idx += 1
            elif c == '!':
                idx += 2
            else:
                non_cancelled_garbage_count += 1
                idx += 1
        elif c == '{':
            depth += 1
            idx += 1
        elif c == '<':
            in_garbage = True
            idx += 1
        elif c == '}':
            total_score += depth
            depth -= 1
            idx += 1
        else:
            idx += 1

    return total_score, non_cancelled_garbage_count


assert analyze('{}') == (1, 0)
assert analyze('{}') == (1, 0)
assert analyze('{{{}}}') == (6, 0)
assert analyze('{{},{}}') == (5, 0)
assert analyze('{{{},{},{{}}}}') == (16, 0)
assert analyze('{<a>,<a>,<a>,<a>}') == (1, 4)
assert analyze('{{<ab>},{<ab>},{<ab>},{<ab>}}') == (9, 8)
assert analyze('{{<!!>},{<!!>},{<!!>},{<!!>}}') == (9, 0)
assert analyze('{{<a!>},{<a!>},{<a!>},{<ab>}}') == (3, 17)

if __name__ == '__main__':
    main()
