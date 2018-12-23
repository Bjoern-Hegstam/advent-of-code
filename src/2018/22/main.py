from collections import namedtuple
from util.geometry import Vector2, get_bounding_box, Direction, Rectangle

ProblemInput = namedtuple('ProblemInput', 'depth, target')

EXAMPLE_INPUT = ProblemInput(510, Vector2(10, 10))
INPUT = ProblemInput(7740, Vector2(12, 763))


class ErosionTile:
    ROCKY = '.'
    WET = '='
    NARROW = '|'


EROSION_TILES = {
    0: ErosionTile.ROCKY,
    1: ErosionTile.WET,
    2: ErosionTile.NARROW
}


def main():
    data = INPUT
    erosion_levels = calc_erosion_levels(data.depth, data.target)
    draw_erosion(erosion_levels)

    risk_levels = {p: erosion_level % 3 for p, erosion_level in erosion_levels.items()}
    risk_level_bounding_box = Rectangle(0, 0, data.target.x + 1, data.target.y + 1)
    total_risk = sum(risk_level for p, risk_level in risk_levels.items() if risk_level_bounding_box.contains(p))

    print('Answer part 1: {}'.format(total_risk))


def calc_erosion_levels(depth, target_coordinate):
    assert depth > 0
    assert target_coordinate.x >= 0 and target_coordinate.y >= 0

    geo_indices = {}

    for x in range(target_coordinate.x + 1):
        geo_indices[Vector2(x, 0)] = x * 16807

    for y in range(target_coordinate.y + 1):
        geo_indices[Vector2(0, y)] = y * 48271

    geo_indices[Vector2(0, 0)] = 0
    geo_indices[target_coordinate] = 0

    erosion_levels = {p: calc_erosion_level(geo_index, depth) for p, geo_index in geo_indices.items()}

    for y in range(target_coordinate.y + 1):
        for x in range(target_coordinate.x + 1):
            p = Vector2(x, y)
            if p in erosion_levels:
                continue

            if p not in geo_indices:
                geo_indices[p] = erosion_levels[p + Direction.LEFT] * erosion_levels[p + Direction.UP]
            erosion_levels[p] = calc_erosion_level(geo_indices[p], depth)

    return erosion_levels


def calc_erosion_level(geo_index, depth):
    return (geo_index + depth) % 20183


def draw_erosion(erosion_levels):
    bounding_box = get_bounding_box(erosion_levels.keys())
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            p = Vector2(bounding_box.x + dx, bounding_box.y + dy)
            print(EROSION_TILES[erosion_levels[p] % 3], end='')
        print('')


if __name__ == '__main__':
    main()
