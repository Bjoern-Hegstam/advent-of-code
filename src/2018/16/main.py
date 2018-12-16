import operator
from collections import namedtuple


REGISTER_COUNT = 4

Sample = namedtuple('Sample', 'before, instruction, after')
Opcode = namedtuple('Opcode', 'name, execute')


def input_a(params):
    return params[0]


def input_b(params):
    return params[1]


def output(params):
    return params[2]


OPCODES = [
    Opcode('addr', lambda registers, params: [registers[input_a(params)] + registers[input_b(params)] if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('addi', lambda registers, params: [registers[input_a(params)] + input_b(params) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),

    Opcode('mulr', lambda registers, params: [registers[input_a(params)] * registers[input_b(params)] if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('muli', lambda registers, params: [registers[input_a(params)] * input_b(params) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),

    Opcode('banr', lambda registers, params: [registers[input_a(params)] & registers[input_b(params)] if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('bani', lambda registers, params: [registers[input_a(params)] & input_b(params) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),

    Opcode('borr', lambda registers, params: [registers[input_a(params)] | registers[input_b(params)] if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('bori', lambda registers, params: [registers[input_a(params)] | input_b(params) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),

    Opcode('setr', lambda registers, params: [registers[input_a(params)] if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('seti', lambda registers, params: [input_a(params) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),

    Opcode('gtir', lambda registers, params: [(1 if input_a(params) > registers[input_b(params)] else 0) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('gtri', lambda registers, params: [(1 if registers[input_a(params)] > input_b(params) else 0) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('gtrr', lambda registers, params: [(1 if registers[input_a(params)] > registers[input_b(params)] else 0) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),

    Opcode('eqir', lambda registers, params: [(1 if input_a(params) == registers[input_b(params)] else 0) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('eqri', lambda registers, params: [(1 if registers[input_a(params)] == input_b(params) else 0) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
    Opcode('eqrr', lambda registers, params: [(1 if registers[input_a(params)] == registers[input_b(params)] else 0) if output(params) == idx else registers[idx] for idx in range(REGISTER_COUNT)]),
]


def main():
    example_sample = Sample([3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1])
    print('Possible opcodes for sample input: {}'.format(find_possible_opcodes(example_sample)))

    samples = load_samples('input_samples')

    possible_opcodes_per_sample = [(sample, find_possible_opcodes(sample)) for sample in samples]

    print('Answer part 1: {}'.format(len([sample for sample, possible_opcodes in possible_opcodes_per_sample if len(possible_opcodes) >= 3])))
    print('')

    opcodes_per_possible_idx = {}
    for sample, possible_opcodes in possible_opcodes_per_sample:
        for possible_opcode in possible_opcodes:
            opcodes_per_possible_idx.setdefault(sample.instruction[0], set()).add(possible_opcode)

    print('Opcodes per potential idx:')
    for idx, opcodes in opcodes_per_possible_idx.items():
        print('{}: [{}]'.format(idx, ', '.join([opcode.name for opcode in opcodes])))
    print('')

    matched_idx_per_opcode = match_opcode_to_indices(opcodes_per_possible_idx)
    opcode_per_idx = {idx: opcode for opcode, idx in matched_idx_per_opcode.items()}

    print('Matched opcodes:')
    for assigned_idx in sorted(opcode_per_idx.keys()):
        print('{}: {}'.format(assigned_idx, opcode_per_idx[assigned_idx].name))
    print()

    program = load_program('input_test_program')
    registers = [0] * REGISTER_COUNT
    for instruction in program:
        registers = opcode_per_idx[instruction[0]].execute(registers, instruction[1:])
    print('Registers after running program: {}'.format(registers))

    print('Answer part 2: {}'.format(registers[0]))


def load_samples(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if len(line.strip()) > 0]

    samples = []
    for i in range(0, len(lines), 3):
        before = [int(n) for n in lines[i][9:-1].split(', ')]
        instruction = [int(n) for n in lines[i + 1].split()]
        after = [int(n) for n in lines[i + 2][9:-1].split(', ')]

        samples.append(Sample(before, instruction, after))

    return samples


def find_possible_opcodes(sample):
    opcode_results = [(opcode, opcode.execute(sample.before, sample.instruction[1:])) for opcode in OPCODES]
    return [opcode for opcode, after in opcode_results if after == sample.after]


def match_opcode_to_indices(opcodes_per_possible_idx):
    # Based on example here: https://www.geeksforgeeks.org/maximum-bipartite-matching/
    matched_idx_per_opcode = {}
    for idx in opcodes_per_possible_idx.keys():
        match_found = match_idx_to_opcode(opcodes_per_possible_idx, idx, set(), matched_idx_per_opcode)
        assert match_found

    return matched_idx_per_opcode


def match_idx_to_opcode(opcodes_per_possible_idx, current_idx, seen_opcodes, matched_idx_per_opcode):
    for opcode in opcodes_per_possible_idx[current_idx]:
        if opcode not in seen_opcodes:
            seen_opcodes.add(opcode)

            if opcode not in matched_idx_per_opcode or match_idx_to_opcode(opcodes_per_possible_idx, matched_idx_per_opcode[opcode], seen_opcodes, matched_idx_per_opcode):
                matched_idx_per_opcode[opcode] = current_idx
                return True

    return False


def load_program(filename):
    print('Loading program: {}'.format(filename))
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if len(line.strip()) > 0]

    return [[int(n) for n in line.split()] for line in lines]


if __name__ == '__main__':
    main()
