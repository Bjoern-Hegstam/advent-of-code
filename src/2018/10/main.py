import re
from collections import namedtuple

from util.geometry import Vector2, get_bounding_box

input_pattern = re.compile(r'position=<\s*(?P<p_x>-?\d+),\s*(?P<p_y>-?\d+)> velocity=<\s*(?P<v_x>-?\d+),\s*(?P<v_y>-?\d+)>')
Light = namedtuple('Light', 'position, velocity')


def main():
    with open('input') as f:
        lines = f.readlines()

    lights = [parse_light(line) for line in lines]
    lights = update_lights(lights, 10136)
    draw_lights(lights)


def parse_light(line):
    match = input_pattern.match(line)
    assert match
    return Light(Vector2(int(match.group('p_x')), int(match.group('p_y'))), Vector2(int(match.group('v_x')), int(match.group('v_y'))))


assert parse_light('position=< -9951, -50547> velocity=< 1,  5>') == Light(Vector2(-9951, -50547), Vector2(1, 5))


def draw_lights(lights):
    positions = set(light.position for light in lights)
    bounding_box = get_bounding_box(positions)
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            if Vector2(bounding_box.x + dx, bounding_box.y + dy) in positions:
                print('#', end='')
            else:
                print('.', end='')
        print('')


def update_lights(lights, step):
    return [
        Light(
            Vector2(
                light.position.x + light.velocity.x * step,
                light.position.y + light.velocity.y * step,
            ),
            light.velocity
        ) for light in lights
    ]


if __name__ == '__main__':
    main()
