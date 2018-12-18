from collections import deque

from util.geometry import Vector2, get_bounding_box, Direction, Rectangle

DEBUG = True

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
    exhausted_springs = set()
    water_tile_counts = 0
    iterations = 0

    while springs:
        spring = springs.pop()

        if DEBUG:
            print('')
            print('Iteration {}'.format(iterations + 1))
            print('Spring count: {}'.format(len(springs) + 1))
            print('Before drip from spring: {}'.format(spring))
            draw(ground_map, Rectangle(spring.x - 50, spring.y - 2, 100, 50))
            print('')

        new_springs = drip_from_spring(ground_map, bounding_box.y + bounding_box.height, spring)

        active_new_springs = [new_spring for new_spring in new_springs if new_spring not in exhausted_springs]
        if len(active_new_springs) == 1 and spring in active_new_springs:
            active_new_springs = []

        if DEBUG:
            print('After drip:')
            draw(ground_map, Rectangle(spring.x - 50, spring.y - 2, 100, 50))
            print('')
            print('New springs: {}'.format(new_springs))
            print('Of which are active: {}'.format(active_new_springs))

        if active_new_springs:
            springs.extend(active_new_springs)
        else:
            exhausted_springs.add(spring)

        updated_water_tile_counts = count_water_tiles_by_type(ground_map, bounding_box.y, bounding_box.y + bounding_box.height)
        if updated_water_tile_counts == water_tile_counts and len(active_new_springs) == 1:
            # TODO: This condition is wrong, simulation is stopped too early
            break
        else:
            water_tile_counts = updated_water_tile_counts

        iterations += 1

        print('{}: {}, sum={}'.format(iterations, water_tile_counts, sum(water_tile_counts.values())))

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
        print('{: 4d}'.format(bounding_box.y + dy), end='')
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
            fill_position = water_position
            while fill_position.y >= spring_position.y:
                left_pour_stop_position, left_pours_down = pour_horizontally(ground_map, fill_position, Direction.LEFT)
                right_pour_stop_position, right_pours_down = pour_horizontally(ground_map, fill_position, Direction.RIGHT)

                if not left_pours_down and not right_pours_down:
                    for x in range(left_pour_stop_position.x, right_pour_stop_position.x + 1):
                        ground_map[Vector2(x, left_pour_stop_position.y)] = Tile.HORIZONTAL_WATER
                    fill_position += Direction.UP
                else:
                    springs = []

                    if fill_position.y != spring_position.y:
                        springs.append(spring_position)

                    if left_pours_down:
                        springs.append(left_pour_stop_position)

                    if right_pours_down:
                        springs.append(right_pour_stop_position)

                    return springs
            return []


def pour_horizontally(ground_map, spring_position, pour_direction):
    seek_position = spring_position + pour_direction

    while not is_position_occupied(ground_map, seek_position):
        ground_map[seek_position] = Tile.VERTICAL_WATER

        if not is_position_occupied(ground_map, seek_position + Direction.DOWN):
            return seek_position, True
        else:
            seek_position += pour_direction

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
