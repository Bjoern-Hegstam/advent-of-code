from collections import namedtuple

from util.geometry import Vector2, get_bounding_box, Direction
from util.path import multi_bfs_search

DEBUG = False


class BoardMarker:
    WALL = '#'
    OPEN_CAVERN = '.'
    ELF = 'E'
    GOBLIN = 'G'


CombatResult = namedtuple('CombatResult', 'completed_rounds_count, sum_of_remaining_hp, elf_died, elf_attack_power')


class Actor:
    def __init__(self, marker, position):
        self.marker = marker
        self.position = position
        self.hp = 200
        self.attack_power = 3

    def __repr__(self):
        return 'Actor[marker={}, position={}, hp={}]'.format(self.marker, self.position, self.hp)


def main():
    first_combat_result = simulate_combat('input')
    print('Answer part 1: {}'.format(first_combat_result.completed_rounds_count * first_combat_result.sum_of_remaining_hp))

    optimal_combat_result = find_optimal_elf_attack_power('input')
    print('Answer part 2: {}'.format(optimal_combat_result.completed_rounds_count * optimal_combat_result.sum_of_remaining_hp))


def find_optimal_elf_attack_power(filename):
    elf_attack_power = 4

    while True:
        combat_result = simulate_combat(filename, elf_attack_power=elf_attack_power, stop_after_first_elf_death=True)
        if combat_result.elf_died:
            elf_attack_power += 1
        else:
            return combat_result


def simulate_combat(filename, elf_attack_power=3, stop_after_first_elf_death=False):
    print('Simulating combat[filename={}, elf_attack_power={}, stop_after_first_elf_death={}]'.format(filename, elf_attack_power, stop_after_first_elf_death))

    board, actors = load_combat_setup(filename)

    for actor in actors:
        if actor.marker == BoardMarker.ELF:
            actor.attack_power = elf_attack_power

    completed_rounds_count = 0

    if DEBUG:
        print('Initially:'.format(completed_rounds_count))
        draw(board, actors)
        print('')

    while True:
        actors, eliminated_actors, full_round_completed = tick(board, actors)
        elf_has_died = BoardMarker.ELF in {actor.marker for actor in eliminated_actors}

        if not full_round_completed:
            if DEBUG:
                print('Round {} aborted prematurely'.format(completed_rounds_count + 1))
                draw(board, actors)
                print('')
            break

        if stop_after_first_elf_death and elf_has_died:
            elf_has_died = True
            break

        completed_rounds_count += 1

        if DEBUG:
            print('After {} round(s):'.format(completed_rounds_count))
            draw(board, actors)
            print('')

    sum_of_remaining_hit_points = sum(actor.hp for actor in actors)

    combat_result = CombatResult(completed_rounds_count, sum_of_remaining_hit_points, elf_has_died, elf_attack_power)
    print('simulate_combat[{}] => {}'.format(filename, combat_result))
    return combat_result


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
                    actors.append(Actor(marker, position))

    return board, actors


def draw(board, actors):
    bounding_box = get_bounding_box(board.keys())
    actors_by_position = {actor.position: actor for actor in actors}
    for y in range(bounding_box.height):
        actors_drawn_on_line = []
        for x in range(bounding_box.width):
            position = Vector2(x, y)
            if position in actors_by_position.keys():
                actor = actors_by_position[position]
                print(actor.marker, end='')
                actors_drawn_on_line.append(actor)
            else:
                print(board[position], end='')
        print('   ', end='')
        print(', '.join('{}({})'.format(actor.marker, actor.hp) for actor in actors_drawn_on_line))


def tick(board, actors):
    actors.sort(key=lambda a: (a.position.y, a.position.x))

    for current_actor in actors:
        if current_actor.hp <= 0:
            continue

        remaining_actors = get_living_actors(actors)
        if len({actor.marker for actor in remaining_actors}) < 2:
            # At least one side of the battle has fallen
            return remaining_actors, get_eliminated_actors(actors), False

        actors_by_position = {actor.position: actor for actor in remaining_actors}
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

    return get_living_actors(actors), get_eliminated_actors(actors), True


def get_living_actors(actors):
    return [actor for actor in actors if actor.hp > 0]


def get_eliminated_actors(actors):
    return [actor for actor in actors if actor.hp <= 0]


def find_adjacent_target(current_actor, actors_by_position):
    adjacent_targets = []
    for adjacent_position in get_adjacent_positions(current_actor.position):
        if is_target_position(current_actor, adjacent_position, actors_by_position):
            adjacent_targets.append(actors_by_position[adjacent_position])

    adjacent_targets.sort(key=lambda a: (a.hp, a.position.y, a.position.x))
    return adjacent_targets[0] if adjacent_targets else None


def determine_new_position(current_actor, board, actors_by_position):
    target_actor_positions = [p for p, a in actors_by_position.items() if is_target(current_actor, a)]
    possible_move_targets = []
    for target_actor_position in target_actor_positions:
        for adjacent_position in get_adjacent_positions(target_actor_position):
            if is_unoccupied_position(adjacent_position, board, actors_by_position):
                possible_move_targets.append(adjacent_position)

    paths = multi_bfs_search(
        current_actor.position,
        lambda p: [adjacent_position for adjacent_position in get_adjacent_positions(p) if is_unoccupied_position(adjacent_position, board, actors_by_position)],
        possible_move_targets
    )

    paths.sort(key=lambda p: (p[-1].y, p[-1].x))

    # First position of each path is our current position, i.e. we will move to the second position of the first path
    return paths[0][1] if paths else None


def get_adjacent_positions(position):
    for direction in [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]:
        yield position + direction


def is_unoccupied_position(position, board, actors_by_position):
    return board.get(position, BoardMarker.WALL) == BoardMarker.OPEN_CAVERN and position not in actors_by_position


def is_adjacent_to_target(current_actor, position, actors_by_position):
    for adjacent_position in get_adjacent_positions(position):
        if is_target_position(current_actor, adjacent_position, actors_by_position):
            return True
    return False


def is_target_position(current_actor, target_position, actors_by_position):
    return is_target(current_actor, actors_by_position[target_position]) if target_position in actors_by_position else False


def is_target(current_actor, possible_target):
    return possible_target.marker != current_actor.marker


assert simulate_combat('example_combat_1') == CombatResult(47, 590, False, 3)
assert simulate_combat('example_combat_2') == CombatResult(37, 982, False, 3)
assert simulate_combat('example_combat_3') == CombatResult(46, 859, False, 3)
assert simulate_combat('example_combat_4') == CombatResult(35, 793, True, 3)
assert simulate_combat('example_combat_5') == CombatResult(54, 536, True, 3)
assert simulate_combat('example_combat_6') == CombatResult(20, 937, True, 3)

assert find_optimal_elf_attack_power('example_combat_1') == CombatResult(29, 172, False, 15)
assert find_optimal_elf_attack_power('example_combat_3') == CombatResult(33, 948, False, 4)
assert find_optimal_elf_attack_power('example_combat_4') == CombatResult(37, 94, False, 15)
assert find_optimal_elf_attack_power('example_combat_5') == CombatResult(39, 166, False, 12)
assert find_optimal_elf_attack_power('example_combat_6') == CombatResult(30, 38, False, 34)

if __name__ == '__main__':
    main()
