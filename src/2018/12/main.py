PLANT = '#'
EMPTY = '.'


def main():
    with open('input') as f:
        lines = f.readlines()

    initial_state_string = lines[0][15:].strip()
    initial_state = dict(zip(range(len(initial_state_string)), initial_state_string))
    state_transitions = {k: v for k, v in [line.strip().split(' => ') for line in lines[2:]]}
    assert state_transitions.get(EMPTY * 5, EMPTY) == EMPTY  # Would be impossible to solve if plants can grow from nothing

    print_state(0, initial_state)
    print(state_transitions)

    state = initial_state
    for generation in range(1, 21):
        state = generate_next_state(state, state_transitions)
        print_state(generation, state)

    pot_sum = sum(idx for idx, char in state.items() if is_plant(char))
    print('Answer part 1: {}'.format(pot_sum))


def generate_next_state(state, state_transitions):
    min_plant_index = min(idx for idx, char in state.items() if is_plant(char))
    max_plant_index = max(idx for idx, char in state.items() if is_plant(char))
    new_state = {}

    for idx in range(min_plant_index - 2, max_plant_index + 3):
        local_state = state.get(idx - 2, EMPTY) \
                      + state.get(idx - 1, EMPTY) \
                      + state.get(idx, EMPTY) \
                      + state.get(idx + 1, EMPTY) \
                      + state.get(idx + 2, EMPTY)
        new_state[idx] = state_transitions.get(local_state, EMPTY)

    return new_state


def is_plant(c):
    return c == PLANT


def print_state(generation, state):
    print('{: 2d}: '.format(generation), end='')
    for idx in sorted(state.keys()):
        print(state[idx], end='')
    print('')


if __name__ == '__main__':
    main()
