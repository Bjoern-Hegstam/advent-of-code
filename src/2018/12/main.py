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

    gen_twenty_pot_sum = None
    stable_generation = None
    stable_plant_drift = None
    target_max_generation = 50000000000

    state = initial_state
    for generation in range(1, target_max_generation):
        prev_state = state
        state = generate_next_state(prev_state, state_transitions)

        print_state(generation, state)

        if generation == 20:
            gen_twenty_pot_sum = sum(idx for idx, char in state.items() if is_plant(char))
        elif do_states_have_same_shape(state, prev_state):
            stable_generation = generation
            stable_plant_drift = get_min_plant_index(state) - get_min_plant_index(prev_state)
            break

    assert gen_twenty_pot_sum == 3241
    print('Answer part 1: {}'.format(gen_twenty_pot_sum))

    remaining_generations = target_max_generation - stable_generation
    stable_plant_indices = get_plant_indices(state)
    stable_pot_sum = sum(idx + remaining_generations * stable_plant_drift for idx in stable_plant_indices)
    print('Plant formation stabilized to {} plants in generation {}, plant drift per generation={}'.format(len(stable_plant_indices), stable_generation, stable_plant_drift))
    assert stable_pot_sum == 2749999999911
    print('Answer part 2: {}'.format(stable_pot_sum))


def generate_next_state(state, state_transitions):
    min_plant_index = get_min_plant_index(state)
    max_plant_index = get_max_plant_index(state)
    new_state = {}

    for idx in range(min_plant_index - 2, max_plant_index + 3):
        local_state = state.get(idx - 2, EMPTY) \
                      + state.get(idx - 1, EMPTY) \
                      + state.get(idx, EMPTY) \
                      + state.get(idx + 1, EMPTY) \
                      + state.get(idx + 2, EMPTY)
        new_state[idx] = state_transitions.get(local_state, EMPTY)

    return new_state


def get_max_plant_index(state):
    max_plant_index = max(get_plant_indices(state))
    return max_plant_index


def get_min_plant_index(state):
    min_plant_index = min(get_plant_indices(state))
    return min_plant_index


def get_plant_indices(state):
    return list(idx for idx, char in state.items() if is_plant(char))


def is_plant(c):
    return c == PLANT


def print_state(generation, state):
    print('{: 2d}: '.format(generation), end='')
    for idx in sorted(state.keys()):
        print(state[idx], end='')
    print('')


def do_states_have_same_shape(state1, state2):
    if len(state1) != len(state2):
        return False

    state1_str = ''.join(state1[idx] for idx in sorted(state1.keys()))
    state2_str = ''.join(state2[idx] for idx in sorted(state2.keys()))

    return state1_str == state2_str


if __name__ == '__main__':
    main()
