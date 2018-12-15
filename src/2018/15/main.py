from collections import namedtuple

from util.geometry import Vector2, get_bounding_box

DEBUG = True


class BoardMarker:
    WALL = '#'
    OPEN_CAVERN = '.'
    ELF = 'E'
    GOBLIN = 'G'


Actor = namedtuple('Actor', 'marker, position, hp')


def main():
    pass


def simulate_combat(filename):
    board, actors = load_combat_setup(filename)

    completed_rounds_count = 0

    if DEBUG:
        print('Round {}'.format(completed_rounds_count))
        draw(board, actors)

    while True:
        actors, full_round_completed = tick(board, actors)
        if not full_round_completed:
            if DEBUG:
                print('Round {} aborted prematurely'.format(completed_rounds_count + 1))
            break
        completed_rounds_count += 1

        if DEBUG:
            print('Round {}'.format(completed_rounds_count))
            draw(board, actors)

    sum_of_remaining_hit_points = 0

    print('simulate_combat[] => completed_rounds_count={}, sum_of_remaining_hit_points={}'.format(filename, completed_rounds_count, sum_of_remaining_hit_points))
    return completed_rounds_count, sum_of_remaining_hit_points


def load_combat_setup(filename):
    board = {}
    actors = []

    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    for y, line in enumerate(lines):
        for x, marker in enumerate(line):
            position = Vector2(x, y)
            if marker == BoardMarker.WALL:
                board[position] = BoardMarker.WALL
            else:
                board[position] = BoardMarker.OPEN_CAVERN
                if marker == BoardMarker.ELF or marker == BoardMarker.GOBLIN:
                    actors.append(Actor(marker, position, 200))

    return board, actors


def draw(board, actors):
    bounding_box = get_bounding_box(board.keys())
    actor_markers = {actor.position: actor.marker for actor in actors}
    for y in range(bounding_box.height):
        for x in range(bounding_box.width):
            position = Vector2(x, y)
            if position in actor_markers.keys():
                print(actor_markers[position], end='')
            else:
                print(board[position], end='')
        print('')


def tick(board, actors):
    full_round_completed = True
    updated_actors = []

    return updated_actors, full_round_completed


assert simulate_combat('example_combat_1') == 47, 590

if __name__ == '__main__':
    main()
