from collections import deque

from util.geometry import Vector2, get_bounding_box, Direction

DEBUG = False

SPRING_POSITION = Vector2(500, 0)


class Tile:
    CLAY = '#'
    SAND = ' '
    WATER_SPRING = '+'
    VERTICAL_WATER = '|'
    HORIZONTAL_WATER = '~'


def main():
    ground_map = load_ground_map('input')
    bounding_box = get_bounding_box(ground_map)

    ground_map[SPRING_POSITION] = Tile.WATER_SPRING

    springs = deque()
    springs.append(SPRING_POSITION)
    water_tile_counts = 0
    iterations = 0
    while True:
        spring = springs.pop()
        new_springs = drip_from_spring(ground_map, bounding_box.y + bounding_box.height, spring)
        if spring in new_springs:
            springs.append(spring)
        elif new_springs:
            springs.append(spring)
            springs.extend(new_springs)

        print('Spring count: {}'.format(len(springs)))

        updated_water_tile_counts = count_water_tiles_by_type(ground_map, bounding_box.y, bounding_box.y + bounding_box.height)
        if updated_water_tile_counts == water_tile_counts and False:
            # TODO: This condition is wrong, simulation is stopped too early
            break
        else:
            water_tile_counts = updated_water_tile_counts

        iterations += 1

        print('{}: {}, sum={}'.format(iterations, water_tile_counts, sum(water_tile_counts.values())))
        if DEBUG:
            draw(ground_map, bounding_box.pad(2))
            print('')

    draw(ground_map, bounding_box.pad(2))
    print('Stabilized at {} water tiles after {} iterations'.format(sum(water_tile_counts.values()), iterations))


def load_ground_map(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    ground_map = {}

    for line in lines:
        coord_parts = sorted(line.split(', '), key=lambda v: v[0])
        assert coord_parts[0][0:2] == 'x='
        assert coord_parts[1][0:2] == 'y='

        for x in parse_range(coord_parts[0][2:]):
            for y in parse_range(coord_parts[1][2:]):
                ground_map[Vector2(x, y)] = Tile.CLAY

    return ground_map


def parse_range(range_str):
    if '..' in range_str:
        parts = range_str.split('..')
        return range(int(parts[0]), int(parts[1]) + 1)
    return range(int(range_str), int(range_str) + 1)


def draw(ground_map, bounding_box):
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            p = Vector2(bounding_box.x + dx, bounding_box.y + dy)
            print(ground_map.get(p, Tile.SAND), end='')
        print('')


def drip_from_spring(ground_map, max_y, spring_position):
    water_position = spring_position
    if spring_position in ground_map and ground_map[spring_position] == Tile.HORIZONTAL_WATER:
        return []

    while True:
        position_below = water_position + Direction.DOWN
        if position_below.y > max_y:
            return []

        tile_below = ground_map.get(position_below, Tile.SAND)

        if tile_below == Tile.SAND or tile_below == Tile.VERTICAL_WATER:
            ground_map[position_below] = Tile.VERTICAL_WATER
            water_position = position_below
        elif tile_below == Tile.CLAY or tile_below == Tile.HORIZONTAL_WATER:
            left_pour_final_position, left_is_new_spring = pour_horizontally(ground_map, water_position, Direction.LEFT)
            right_pour_final_position, right_is_new_spring = pour_horizontally(ground_map, water_position, Direction.RIGHT)

            new_springs = []
            if left_is_new_spring:
                new_springs.append(left_pour_final_position)

            if right_is_new_spring:
                new_springs.append(right_pour_final_position)

            if new_springs:
                return new_springs

            final_water_destinations = {water_position}
            final_water_destinations.add(left_pour_final_position)
            final_water_destinations.add(right_pour_final_position)

            # No more open space to pour into
            if len(final_water_destinations) == 1:
                ground_map[water_position] = Tile.HORIZONTAL_WATER

            return [spring_position]


def pour_horizontally(ground_map, spring_position, pour_direction):
    seek_position = spring_position + pour_direction

    while not is_position_occupied(ground_map, seek_position):
        ground_map[seek_position] = Tile.VERTICAL_WATER

        if not is_position_occupied(ground_map, seek_position + Direction.DOWN):
            return seek_position, True
        else:
            seek_position += pour_direction

    final_position = seek_position - pour_direction
    if final_position != spring_position:
        ground_map[final_position] = Tile.HORIZONTAL_WATER

    return seek_position - pour_direction, False


def is_position_occupied(ground_map, position):
    tile = ground_map.get(position, Tile.SAND)
    return tile == Tile.CLAY or tile == Tile.HORIZONTAL_WATER


def count_water_tiles_by_type(ground_map, min_y, max_y):
    tile_counts = {}
    for p, tile in ground_map.items():
        if min_y <= p.y < max_y and (tile == Tile.HORIZONTAL_WATER or tile == Tile.VERTICAL_WATER):
            tile_counts[tile] = tile_counts.get(tile, 0) + 1
    return tile_counts


if __name__ == '__main__':
    main()
