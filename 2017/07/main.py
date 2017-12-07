import re


def main():
    with open('input') as f:
        lines = f.readlines()
    programs = build_program_tree(lines)

    print('Answer part 1: {}'.format(solve_part_one(programs)))
    print('Answer part 2: {}'.format(solve_part_two(programs)))


def solve_part_one(programs):
    bottoms = [name for name, program in programs.items() if not program.parent]
    assert len(bottoms) == 1
    return bottoms[0]


def build_program_tree(lines):
    programs = {}
    for line in lines:
        match = re.match('(?P<name>\w+) \((?P<weight>\d+)\)( -> (?P<children>[,\s\w]+))?', line.strip())
        if match:
            name = match.group('name')
            weight = int(match.group('weight'))
            p = programs.setdefault(name, ProgramData(name))
            p.weight = weight

            if match.groupdict()['children']:
                for child_name in match.group('children').split(', '):
                    child = programs.setdefault(child_name, ProgramData(child_name))
                    child.parent = p
                    p.children.append(child)
    return programs


def solve_part_two(programs):
    root = [p for p in programs.values() if not p.parent][0]

    current_program = root
    while True:
        unbalanced_child, expected_weight = find_unbalanced(current_program.children)
        if not unbalanced_child.children:
            return expected_weight

        unbalanced_grandchild, _ = find_unbalanced(unbalanced_child.children)
        if not unbalanced_grandchild:
            return expected_weight - sum(get_disc_weight(c) for c in unbalanced_child.children)
        else:
            current_program = unbalanced_child


disc_weights = {}


def get_disc_weight(program):
    if program.name in disc_weights:
        return disc_weights[program.name]

    if program.children:
        child_weights = sum(get_disc_weight(child) for child in program.children)
    else:
        child_weights = 0

    return disc_weights.setdefault(
        program.name,
        program.weight + child_weights
    )


def find_unbalanced(programs):
    weights = [(p, get_disc_weight(p)) for p in programs]
    disc_weight_hist = {}
    for p, disc_weight in weights:
        disc_weight_hist[disc_weight] = disc_weight_hist.get(disc_weight, 0) + 1

    if len(disc_weight_hist) == 1:
        return None, weights[0][1]

    for p, disc_weight in weights:
        if disc_weight_hist[disc_weight] == 1:
            return p, max(disc_weight_hist, key=disc_weight_hist.get)


class ProgramData:
    def __init__(self, name):
        self.name = name
        self.weight = None
        self.parent = None
        self.children = []

    def __repr__(self) -> str:
        return 'ProgramData(name={}, weight={}, parent={}, children=[{})'.format(
            self.name,
            self.weight,
            self.parent,
            ', '.join([p.name for p in self.children])
        )


test_input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

test_programs = build_program_tree(test_input.splitlines())
assert solve_part_one(test_programs) == 'tknk'

assert solve_part_two(test_programs) == 60


if __name__ == '__main__':
    main()
