from collections import namedtuple

from util.geometry import Vector2, get_bounding_box

DEBUG = True

Train = namedtuple('Train', 'id, position, direction, turn_count')


class Directions:
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)


RAIL_DIRECTIONS_PER_CHAR = {
    '/': {
        Directions.UP: Directions.RIGHT,
        Directions.DOWN: Directions.LEFT,
        Directions.LEFT: Directions.DOWN,
        Directions.RIGHT: Directions.UP
    },
    '\\': {
        Directions.UP: Directions.LEFT,
        Directions.DOWN: Directions.RIGHT,
        Directions.LEFT: Directions.UP,
        Directions.RIGHT: Directions.DOWN
    },
    '|': {
        Directions.UP: Directions.UP,
        Directions.DOWN: Directions.DOWN
    },
    '-': {
        Directions.LEFT: Directions.LEFT,
        Directions.RIGHT: Directions.RIGHT
    }
}

TRAIN_DIRECTIONS_PER_CHAR = {
    '^': Directions.UP,
    'v': Directions.DOWN,
    '<': Directions.LEFT,
    '>': Directions.RIGHT
}

TRAIN_CHAR_PER_DIRECTION = {v: k for k, v in TRAIN_DIRECTIONS_PER_CHAR.items()}

CROSSING = '+'


def main():
    base_input = 'input'
    with open(base_input) as f:
        lines = f.readlines()

    with open('{}_without_trains'.format(base_input)) as f:
        lines_without_trains = f.readlines()

    railroad, trains = parse_input(
        [line.rstrip() for line in lines_without_trains],
        [line.rstrip() for line in lines]
    )

    if DEBUG:
        draw_railroad(railroad, trains)

    crash_position = solve_part_one(railroad, trains)
    print('Answer part 1: {},{}'.format(crash_position.x, crash_position.y))

    last_cart_position = solve_part_two(railroad, trains)
    print('Answer part 2: {},{}'.format(last_cart_position.x, last_cart_position.y))


def parse_input(lines_without_trains, lines):
    railroad = {}
    trains = []

    for y, line in enumerate(lines_without_trains):
        for x, c in enumerate(line):
            if c != ' ':
                railroad[Vector2(x, y)] = c

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c in TRAIN_DIRECTIONS_PER_CHAR.keys():
                trains.append(Train(len(trains), Vector2(x, y), TRAIN_DIRECTIONS_PER_CHAR[c], 0))

    return railroad, trains


def draw_railroad(railroad, trains):
    bounding_box = get_bounding_box(railroad.keys())
    mapped_trains = {train.position: TRAIN_CHAR_PER_DIRECTION[train.direction] for train in trains}
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            p = Vector2(bounding_box.x + dx, bounding_box.y + dy)
            if p in mapped_trains:
                print(mapped_trains[p], end='')
            elif p in railroad:
                print(railroad[p], end='')
            else:
                print(' ', end='')
        print('')


def solve_part_one(railroad, initial_trains):
    tick_count = 0
    trains = initial_trains
    while True:
        trains, crash_position = tick(railroad, trains)
        if crash_position:
            print('Crash: {}'.format(crash_position))
            break

        tick_count += 1
        if DEBUG:
            print('Tick: {}'.format(tick_count))

    return crash_position


def solve_part_two(railroad, initial_trains):
    tick_count = 0
    trains = initial_trains
    while True:
        trains, crash_position = tick(railroad, trains, remove_crashed_trains=True)
        if crash_position:
            print('Crash: {}'.format(crash_position))
            break

        tick_count += 1
        if DEBUG:
            print('Tick: {}'.format(tick_count))
            print('Train count: {}'.format(len(trains)))

        if len(trains) == 1:
            return trains[0].position


def tick(railroad, trains, remove_crashed_trains=False):
    updated_trains = []
    current_train_positions = {train.id: train.position for train in trains}
    crash_positions = set()

    for train in sorted(trains, key=lambda t: (t.position.y, t.position.x)):
        if train.position in crash_positions:
            continue

        current_rail = railroad[train.position]
        new_direction = None
        turn_count = train.turn_count

        if current_rail == CROSSING:
            turn_count += 1
            if train.turn_count % 3 == 0:
                new_direction = Vector2(train.direction.y, -train.direction.x)
            elif train.turn_count % 3 == 1:
                new_direction = train.direction
            elif train.turn_count % 3 == 2:
                new_direction = Vector2(-train.direction.y, train.direction.x)
        else:
            new_direction = RAIL_DIRECTIONS_PER_CHAR[railroad[train.position]][train.direction]

        new_position = train.position + new_direction
        if new_position in current_train_positions.values():
            if remove_crashed_trains:
                crash_positions.add(new_position)
            else:
                return None, new_position
        current_train_positions[train.id] = new_position
        updated_trains.append(Train(train.id, new_position, new_direction, turn_count))

    if remove_crashed_trains:
        updated_trains = [train for train in updated_trains if train.position not in crash_positions]
    return updated_trains, None


if __name__ == '__main__':
    main()
