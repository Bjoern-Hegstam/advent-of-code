from util.geometry import Vector2, get_bounding_box, Direction

WATER_SPRING_POSITION = Vector2(500, 0)


class Tile:
    CLAY = '#'
    SAND = '.'
    WATER_SPRING = '+'
    VERTICAL_WATER = '|'
    HORIZONTAL_WATER = '~'


def main():
    ground_map = load_ground_map('example_input')
    bounding_box = get_bounding_box(ground_map)

    ground_map[WATER_SPRING_POSITION] = Tile.WATER_SPRING

    water_tile_counts = 0
    iterations = 0
    while True:
        drip_from_spring(ground_map, bounding_box.y + bounding_box.height, WATER_SPRING_POSITION)

        updated_water_tile_counts = count_water_tiles_by_type(ground_map, bounding_box.y, bounding_box.y + bounding_box.height)
        if updated_water_tile_counts == water_tile_counts:
            break
        else:
            water_tile_counts = updated_water_tile_counts

        iterations += 1
        draw(ground_map, bounding_box.pad(2))
        print('')

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
    # Seek downwards
    water_position = spring_position
    while True:
        position_below = water_position + Direction.DOWN
        if position_below.y > max_y:
            return [position_below]

        tile_below = ground_map.get(position_below, Tile.SAND)

        if tile_below == Tile.SAND or tile_below == Tile.VERTICAL_WATER:
            ground_map[position_below] = Tile.VERTICAL_WATER
            water_position = position_below
        elif tile_below == Tile.CLAY or tile_below == Tile.HORIZONTAL_WATER:
            left_pour_destinations = pour_horizontally(ground_map, max_y, water_position, Direction.LEFT)
            right_pour_destinations = pour_horizontally(ground_map, max_y, water_position, Direction.RIGHT)

            final_water_destinations = {water_position}
            final_water_destinations.update(left_pour_destinations)
            final_water_destinations.update(right_pour_destinations)

            # No more open space to pour into
            if len(final_water_destinations) == 1:
                ground_map[water_position] = Tile.HORIZONTAL_WATER
            return list(final_water_destinations)


def pour_horizontally(ground_map, max_y, spring_position, pour_direction):
    seek_position = spring_position + pour_direction

    while not is_position_occupied(ground_map, seek_position):
        ground_map[seek_position] = Tile.VERTICAL_WATER

        if not is_position_occupied(ground_map, seek_position + Direction.DOWN):
            return drip_from_spring(ground_map, max_y, seek_position)
        else:
            seek_position += pour_direction

    final_position = seek_position - pour_direction
    if final_position != spring_position:
        ground_map[final_position] = Tile.HORIZONTAL_WATER

    return [seek_position - pour_direction]


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
