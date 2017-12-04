import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    print('Answer part one: {}'.format(solve_part_one(347991)))
    print('Answer part two: {}'.format(solve_part_two(347991)))


def solve_part_one(val):
    grid = generate_spiral(val)
    for pos, v in grid.items():
        if v == val:
            return abs(pos[0]) + abs(pos[1])
    return -1


def generate_spiral(max_val, val_fun=lambda grid, prev_num, x, y: prev_num + 1):
    x = 0
    y = 0
    grid = {}

    direction = (1, 0)

    n = 0
    num = 1
    current_val = 1
    prev_val = 0

    while prev_val <= max_val:
        grid[(x, y)] = current_val

        if x == n and y == -n:
            n += 1

        if direction[0] == 1 and x == n:
            direction = rot(direction)
        elif direction[0] == -1 and x == -n:
            direction = rot(direction)
        elif direction[1] == 1 and y == n:
            direction = rot(direction)
        elif direction[1] == -1 and y == -n:
            direction = rot(direction)

        x, y = x + direction[0], y + direction[1]

        prev_val = current_val
        current_val = val_fun(grid, num, x, y)
        num += 1
    return grid


def rot(v):
    return -v[1], v[0]


assert solve_part_one(1) == 0
assert solve_part_one(12) == 3
assert solve_part_one(23) == 2
assert solve_part_one(1024) == 31


def solve_part_two(val):
    grid = generate_spiral(val, lambda g, prev_num, x, y: area_sum(g, x, y))
    return max(grid.values())


def area_sum(grid, x0, y0):
    tot = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            tot += grid.get((x0 + dx, y0 + dy), 0)
    return tot


if __name__ == '__main__':
    main()
