def main():
    with open('input') as f:
        blocks = [int(x) for x in f.readline().split()]

        redistribution_cycles, loop_cycles = redistribute_blocks(blocks)
        print('Answer part 1: {}'.format(redistribution_cycles))
        print('Answer part 1: {}'.format(loop_cycles))


def redistribute_blocks(initial_state):
    state = initial_state[:]
    states = {}  # Map state to iteration where it first appeared

    iterations = 0
    while state_hash(state) not in states:
        states[state_hash(state)] = iterations
        iterations += 1

        max_idx, max_val = max(enumerate(state), key=lambda p: p[1])
        idx = (max_idx + 1) % len(state)
        state[max_idx] = 0

        while max_val > 0:
            state[idx] += 1
            max_val -= 1
            idx = (idx + 1) % len(state)

    return iterations, iterations - states[state_hash(state)]


def state_hash(state):
    return ''.join([str(s) for s in state])


assert redistribute_blocks([0, 2, 7, 0]) == (5, 4)


if __name__ == '__main__':
    main()
