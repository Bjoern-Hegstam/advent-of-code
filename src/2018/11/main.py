from util.geometry import Rectangle, get_points, Vector2


def main():
    serial_number = 9306

    max_position, max_power_level = find_largest_power_square(generate_power_grid(serial_number), Rectangle(1, 1, 299, 299))

    print('Answer part one: {},{}'.format(max_position.x, max_position.y))


def generate_power_grid(serial_number):
    grid = {}

    for p in get_points(Rectangle(1, 1, 299, 299)):
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


assert get_hundreds_digit(12345) == 3


def draw_grid(grid, bounding_box):
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
                print('{: d} '.format(grid[Vector2(bounding_box.x + dx, bounding_box.y + dy)]), end='')
        print('')


def find_largest_power_square(power_grid, bounding_box):
    max_power_level = float('-Inf')
    max_position = None

    for dy in range(bounding_box.height - 2):
        for dx in range(bounding_box.width - 2):
            power_level = 0
            for sub_dy in range(3):
                for sub_dx in range(3):
                    power_level += power_grid[Vector2(bounding_box.x + dx + sub_dx, bounding_box.y + dy + sub_dy)]

            if power_level > max_power_level:
                max_power_level = power_level
                max_position = Vector2(bounding_box.x + dx, bounding_box.y + dy)

    return max_position, max_power_level


assert find_largest_power_square(generate_power_grid(18), Rectangle(1, 1, 299, 299)) == (Vector2(33, 45), 29)

if __name__ == '__main__':
    main()
