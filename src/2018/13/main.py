from collections import namedtuple

from util.geometry import Vector2, get_bounding_box

Train = namedtuple('Train', 'position, direction, last_turn_direction')
Rail = namedtuple('Rail', 'char, directions')


class Directions:
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)


RAIL_DIRECTIONS_PER_CHAR = {
    '/': {Directions.DOWN, Directions.RIGHT},
    '\\': {Directions.RIGHT, Directions.DOWN},
    '|': {Directions.UP, Directions.DOWN},
    '-': {Directions.LEFT, Directions.RIGHT},
    '+': {Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT}
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
    with open('example_input') as f:
        lines = f.readlines()

    railroad, trains = parse_input([line.rstrip() for line in lines])
    draw_railroad(railroad, trains)


def parse_input(lines):
    railroad = {}
    trains = []

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ' ':
                continue

            position = Vector2(x, y)
            if c in TRAIN_DIRECTIONS_PER_CHAR.keys():
                trains.append(Train(position, TRAIN_DIRECTIONS_PER_CHAR[c], None))
            else:
                railroad[position] = Rail(c, RAIL_DIRECTIONS_PER_CHAR[c])

    # Figure out rail pieces for positions that were covered by a train
    for train in trains:
        position = train.position
        up = railroad.get(position + Directions.UP)
        down = railroad.get(position + Directions.DOWN)
        left = railroad.get(position + Directions.LEFT)
        right = railroad.get(position + Directions.RIGHT)

        directions = set()
        if up and up.char in '+/\\|':
            directions.add(Directions.UP)
        if down and down.char in '+/\\|':
            directions.add(Directions.DOWN)
        if left and left.char in '+/\\-':
            directions.add(Directions.LEFT)
        if right and right.char in '+/\\-':
            directions.add(Directions.RIGHT)

        for c, dirs in RAIL_DIRECTIONS_PER_CHAR.items():
            if dirs == directions:
                railroad[position] = Rail(c, directions)
                break

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
                print(railroad[p].char, end='')
            else:
                print(' ', end='')
        print('')


if __name__ == '__main__':
    main()
