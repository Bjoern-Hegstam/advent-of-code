import re

from util.geometry import Vector2, get_bounding_box

input_pattern = re.compile(r'position=<\s*(?P<p_x>-?\d+),\s*(?P<p_y>-?\d+)> velocity=<\s*(?P<v_x>-?\d+),\s*(?P<v_y>-?\d+)>')


def main():
    with open('input') as f:
        lines = f.readlines()

    positions = []
    velocities = []

    for line in lines:
        p, v = parse_light(line)
        positions.append(p)
        velocities.append(v)

    elapsed_time = 0
    bounding_box = get_bounding_box(positions)
    min_bounding_box_size = bounding_box.width * bounding_box.height
    while True:
        new_positions = update_lights(positions, velocities, 1)
        bounding_box = get_bounding_box(new_positions)
        bounding_box_size = bounding_box.width * bounding_box.height

        print('Elapsed time={}, Bounding box area={}'.format(elapsed_time, bounding_box_size))

        if bounding_box_size < min_bounding_box_size:
            elapsed_time += 1
            min_bounding_box_size = bounding_box_size
            positions = new_positions
        else:
            break

    draw_lights(positions)
    print('Message appears after {} seconds'.format(elapsed_time))


def parse_light(line):
    match = input_pattern.match(line)
    assert match
    return Vector2(int(match.group('p_x')), int(match.group('p_y'))), Vector2(int(match.group('v_x')), int(match.group('v_y')))


assert parse_light('position=< -9951, -50547> velocity=< 1,  5>') == (Vector2(-9951, -50547), Vector2(1, 5))


def draw_lights(positions):
    bounding_box = get_bounding_box(positions)
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            if Vector2(bounding_box.x + dx, bounding_box.y + dy) in positions:
                print('#', end='')
            else:
                print('.', end='')
        print('')


def update_lights(positions, velocities, step):
    return [Vector2(p.x + v.x * step, p.y + v.y * step,) for p, v in zip(positions, velocities)]


if __name__ == '__main__':
    main()
