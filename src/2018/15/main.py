from util.geometry import Vector2, get_bounding_box, Direction

DEBUG = True


class BoardMarker:
    WALL = '#'
    OPEN_CAVERN = '.'
    ELF = 'E'
    GOBLIN = 'G'


class Actor:
    def __init__(self, marker, position):
        self.marker = marker,
        self.position = position
        self.hp = 200
        self.attack_power = 3

    def __repr__(self):
        return 'Actor[marker={}, position={}, hp={}]'.format(self.marker, self.position, self.hp)


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
    remaining_actor_types = {actor.type for actor in actors}
    if len(remaining_actor_types) < 2:
        # At least one side of the battle has fallen
        return actors, False

    actor_positions = sorted([actor.position for actor in actors], key=lambda a: (a.position.y, a.position.x))
    actors_by_position = {actor.position: actor for actor in actors}

    for actor_position in actor_positions:
        current_actor = actors_by_position[actor_position]
        adjacent_target = find_adjacent_target(current_actor, actors_by_position)

        if not adjacent_target:
            new_position = determine_new_position(current_actor, board, actors_by_position)
            if new_position:
                current_actor.position = new_position
                adjacent_target = find_adjacent_target(current_actor, actors_by_position)
            else:
                # Had no adjacent target and couldn't move to a new position
                continue

        if adjacent_target:
            adjacent_target.hp -= current_actor.attack_power

    return [actor for actor in actors if actor.hp > 0], True


def find_adjacent_target(current_actor, actors_by_position):
    for direction in [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]:
        adjacent_position = current_actor.position + direction
        if adjacent_position in actors_by_position and actors_by_position[adjacent_position].marker != current_actor.marker:
            return actors_by_position[adjacent_position]
    return None


def determine_new_position(current_actor, board, actors_by_position):
    pass


assert simulate_combat('example_combat_1') == 47, 590

if __name__ == '__main__':
    main()
