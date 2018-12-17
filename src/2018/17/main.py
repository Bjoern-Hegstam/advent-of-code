from util.geometry import Vector2, get_bounding_box, pad

WATER_SPRING_POSITION = Vector2(500, 0)


class Marker:
    CLAY = '#'
    SAND = '.'
    WATER_SPRING = '+'
    VERTICAL_WATER = '|'
    HORIZONTAL_WATER = '~'


def main():
    ground_map = load_ground_map('example_input')
    draw(ground_map)


def load_ground_map(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    ground_map = {WATER_SPRING_POSITION: Marker.WATER_SPRING}

    for line in lines:
        coord_parts = sorted(line.split(', '), key=lambda v: v[0])
        assert coord_parts[0][0:2] == 'x='
        assert coord_parts[1][0:2] == 'y='

        for x in parse_range(coord_parts[0][2:]):
            for y in parse_range(coord_parts[1][2:]):
                ground_map[Vector2(x, y)] = Marker.CLAY

    return ground_map


def parse_range(range_str):
    if '..' in range_str:
        parts = range_str.split('..')
        return range(int(parts[0]), int(parts[1]) + 1)
    return range(int(range_str), int(range_str) + 1)


def draw(ground_map):
    bounding_box = pad(get_bounding_box(ground_map.keys()), 1)
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            p = Vector2(bounding_box.x + dx, bounding_box.y + dy)
            print(ground_map.get(p, Marker.SAND), end='')
        print('')


def update(ground_map):
    # Starting from spring
    #  Move down until next tile below is either clay or horizontal water
    #  Then search to the left and right until a wall is encountered or open space/vertical water appears below

    # for each vertical water
    #  if below is SAND => Turn below into vertical water
    #  elif below it CLAY => Turn self into horizontal water
    #  elif below is HORIZONTAL_WATER => Turn self into
    pass


if __name__ == '__main__':
    main()
