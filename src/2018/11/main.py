import operator

from util.geometry import Rectangle, Vector2

GRID_SIZE = 300


def main():
    serial_number = 9306

    power_grid = generate_power_grid(serial_number)
    power_level_sub_matrices = compute_power_level_sub_matrices(power_grid)
    all_power_levels = sum_across_all_square_sizes(power_level_sub_matrices)

    max_position_1, _, _ = find_largest_power_level_sum(all_power_levels)
    assert max_position_1 == Vector2(235, 38)
    print('Answer part one: {},{}'.format(max_position_1.x, max_position_1.y))

    max_position_2, _, max_square_size = find_largest_power_level_sum(all_power_levels, test_all_square_sizes=True)
    assert max_position_2, max_square_size == (Vector2(233, 146), 13)
    print('Answer part two: {},{},{}'.format(max_position_2.x, max_position_2.y, max_square_size))


def generate_power_grid(serial_number):
    print('Generating power grid for serial number {}'.format(serial_number))

    grid = {}

    for p in Rectangle(1, 1, GRID_SIZE, GRID_SIZE).get_points():
        rack_id = p.x + 10
        power_level = rack_id * p.y
        power_level += serial_number
        power_level *= rack_id
        power_level = get_hundreds_digit(power_level)
        power_level -= 5
        grid[p] = power_level

    return grid


def get_hundreds_digit(power_level):
    return (power_level % 1000) // 100


def compute_power_level_sub_matrices(power_grid):
    print('Computing power level sub matrices')
    sub_matrices = {Vector2(1, 1): power_grid[Vector2(1, 1)]}

    for dy in range(GRID_SIZE):
        for dx in range(GRID_SIZE):
            sub_matrices[Vector2(1 + dx, 1 + dy)] = power_grid[Vector2(1 + dx, 1 + dy)] \
                                                    + sub_matrices.get(Vector2(1 + dx, dy), 0) \
                                                    + sub_matrices.get(Vector2(dx, 1 + dy), 0) \
                                                    - sub_matrices.get(Vector2(dx, dy), 0)

    return sub_matrices


def draw_grid(grid, bounding_box):
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
                print('{: d} '.format(grid[Vector2(bounding_box.x + dx, bounding_box.y + dy)]), end='')
        print('')


assert get_hundreds_digit(12345) == 3


def find_largest_power_level_sum(all_power_levels, test_all_square_sizes=False):
    print('Finding largest power level sum')
    if test_all_square_sizes:
        position, grid_size = max(all_power_levels.items(), key=operator.itemgetter(1))[0]
        return position, all_power_levels[(position, grid_size)], grid_size
    else:
        power_levels = {k: v for k, v in all_power_levels.items() if k[1] == 3}
        position, grid_size = max(power_levels.items(), key=operator.itemgetter(1))[0]
        return position, power_levels[(position, grid_size)], grid_size


def sum_across_all_square_sizes(power_level_sub_matrices):
    print('Computing power level sums for all square sizes')
    power_levels = {}

    for square_size in range(1, GRID_SIZE):
        print('square_size={}'.format(square_size))
        for y in range(1, GRID_SIZE + 1 - (square_size - 1)):
            for x in range(1, GRID_SIZE + 1 - (square_size - 1)):
                max_square_size = min(GRID_SIZE + 1 - x, GRID_SIZE + 1 - y)
                if square_size > max_square_size:
                    continue

                position = Vector2(x, y)
                power_levels[(position, square_size)] = calc_power_level(power_level_sub_matrices, position, square_size)

    return power_levels


def calc_power_level(power_level_sub_matrices, position, square_size):
    return power_level_sub_matrices[Vector2(position.x + square_size - 1, position.y + square_size - 1)] \
           - power_level_sub_matrices.get(Vector2(position.x + square_size - 1, position.y - 1), 0) \
           - power_level_sub_matrices.get(Vector2(position.x - 1, position.y + square_size - 1), 0) \
           + power_level_sub_matrices.get(Vector2(position.x - 1, position.y - 1), 0)


all_power_levels_for_example_grid = sum_across_all_square_sizes(compute_power_level_sub_matrices(generate_power_grid(18)))
assert find_largest_power_level_sum(all_power_levels_for_example_grid) == (Vector2(33, 45), 29, 3)
assert find_largest_power_level_sum(all_power_levels_for_example_grid, test_all_square_sizes=True) == (Vector2(90, 269), 113, 16)

if __name__ == '__main__':
    main()
