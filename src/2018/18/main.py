from collections import Counter

from util.geometry import get_bounding_box, Vector2, Direction


class Tile:
    OPEN = '.'
    TREES = '|'
    LUMBER = '#'


def main():
    landscape = load_landscape('input')

    print('Initial state: ')
    draw(landscape)
    print('')

    for minute in range(10):
        landscape = update(landscape)

        print('After {} minute(s):'.format(minute + 1))
        draw(landscape)
        print('')

    tile_count = Counter(landscape.values())
    print('Answer part 1: {}'.format(tile_count.get(Tile.TREES, 0) * tile_count.get(Tile.LUMBER, 0)))


def load_landscape(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    landscape = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            landscape[Vector2(x, y)] = c

    return landscape


def update(landscape):
    updated_landscape = {}
    bounding_box = get_bounding_box(landscape)

    for position in landscape:
        tile = landscape[position]
        neighbor_tiles = Counter(landscape[p] for p in gen_neighbor_positions(position, bounding_box))

        if tile == Tile.OPEN and neighbor_tiles.get(Tile.TREES, 0) >= 3:
            updated_landscape[position] = Tile.TREES
        elif tile == Tile.TREES and neighbor_tiles.get(Tile.LUMBER, 0) >= 3:
            updated_landscape[position] = Tile.LUMBER
        elif tile == Tile.LUMBER:
            if neighbor_tiles.get(Tile.LUMBER, 0) >= 1 and neighbor_tiles.get(Tile.TREES, 0):
                updated_landscape[position] = Tile.LUMBER
            else:
                updated_landscape[position] = Tile.OPEN
        else:
            updated_landscape[position] = landscape[position]

    return updated_landscape


def gen_neighbor_positions(position, bounding_box):
    return [
        p for p in [
            position + Direction.UP,
            position + Direction.UP + Direction.RIGHT,
            position + Direction.RIGHT,
            position + Direction.DOWN + Direction.RIGHT,
            position + Direction.DOWN,
            position + Direction.DOWN + Direction.LEFT,
            position + Direction.LEFT,
            position + Direction.LEFT + Direction.UP
        ] if bounding_box.contains(p)
    ]


def draw(landscape):
    bounding_box = get_bounding_box(landscape.keys())
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            p = Vector2(bounding_box.x + dx, bounding_box.y + dy)
            print(landscape[p], end='')
        print('')


if __name__ == '__main__':
    main()
