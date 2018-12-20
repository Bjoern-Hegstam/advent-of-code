from collections import Counter

from util.geometry import get_bounding_box, Vector2, Direction

DEBUG = False


class Tile:
    OPEN = '.'
    TREES = '|'
    LUMBER = '#'


def main():
    initial_landscape = load_landscape('input')

    print('Initial state: ')
    draw(initial_landscape)
    print('')

    landscape = run_simulation(initial_landscape, 10)
    tile_count = Counter(landscape.values())
    print('Answer part 1: {}'.format(tile_count.get(Tile.TREES, 0) * tile_count.get(Tile.LUMBER, 0)))

    landscape = run_simulation(initial_landscape, 1000000000)
    tile_count = Counter(landscape.values())
    print('Answer part 2: {}'.format(tile_count.get(Tile.TREES, 0) * tile_count.get(Tile.LUMBER, 0)))


def load_landscape(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    landscape = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            landscape[Vector2(x, y)] = c

    return landscape


def run_simulation(initial_landscape, iter_count):
    landscape = initial_landscape
    previous_landscapes = [landscape]
    iteration = 0
    while iteration < iter_count:
        landscape = update(landscape)
        iteration += 1

        for idx, old_landscape in enumerate(previous_landscapes):
            if old_landscape == landscape:
                cycle_length = iteration - idx
                print('Found landscape cycle of length {}'.format(cycle_length))
                # Found a cycle, infer which landscape will be current on the last iteration
                cycle_offset = cycle_length % len(previous_landscapes)
                return previous_landscapes[idx + cycle_offset - 1]
        else:
            previous_landscapes.append(landscape)
            print('Iteration {}: Landscape count={}'.format(iteration, len(previous_landscapes)))

        if DEBUG:
            draw(landscape)

    return landscape


def update(landscape):
    updated_landscape = {}
    bounding_box = get_bounding_box(landscape)

    cumulative_tile_counts = {}
    for dy in range(bounding_box.height + 1):
        for dx in range(bounding_box.width + 1):
            p = Vector2(bounding_box.x + dx, bounding_box.y + dy)
            cumulative_tile_counts[p] = (Counter(landscape[p]) if p in landscape else Counter()) \
                                        + cumulative_tile_counts.get(p + Direction.UP, Counter()) \
                                        + cumulative_tile_counts.get(p + Direction.LEFT, Counter()) \
                                        - cumulative_tile_counts.get(p + Direction.LEFT + Direction.UP, Counter())

    for position in landscape:
        tile = landscape[position]
        neighbor_tiles = cumulative_tile_counts.get(position + Vector2(1, 1), Counter()) \
                         + cumulative_tile_counts.get(position + Vector2(-2, -2), Counter()) \
                         - cumulative_tile_counts.get(position + Vector2(1, -2), Counter()) \
                         - cumulative_tile_counts.get(position + Vector2(-2, 1), Counter()) \
                         - Counter(tile)
        assert sum(neighbor_tiles.values()) <= 8

        if tile == Tile.OPEN and neighbor_tiles.get(Tile.TREES, 0) >= 3:
            updated_landscape[position] = Tile.TREES
        elif tile == Tile.TREES and neighbor_tiles.get(Tile.LUMBER, 0) >= 3:
            updated_landscape[position] = Tile.LUMBER
        elif tile == Tile.LUMBER:
            if neighbor_tiles.get(Tile.LUMBER, 0) >= 1 and neighbor_tiles.get(Tile.TREES, 0) >= 1:
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
