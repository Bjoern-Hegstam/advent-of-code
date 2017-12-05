def main():
    with open('input') as f:
        lines = f.readlines()

    instructions = [int(n) for n in lines]
    print('Answer part 1: {}'.format(steps_to_exit(instructions)))
    print('Answer part 2: {}'.format(steps_to_exit(instructions, special_offset=True)))


def steps_to_exit(instructions, special_offset=False):
    instructions = instructions[:]
    idx = 0
    steps = 0
    while idx < len(instructions):
        prev_idx = idx
        offset = instructions[idx]
        idx += offset

        if special_offset and offset >= 3:
            instructions[prev_idx] -= 1
        else:
            instructions[prev_idx] += 1

        steps += 1
    return steps


assert steps_to_exit([0, 3, 0, 1, -3]) == 5
assert steps_to_exit([0, 3, 0, 1, -3], special_offset=True) == 10


if __name__ == '__main__':
    main()
