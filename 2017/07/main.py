import re


def main():
    with open('input') as f:
        lines = f.readlines()
    print('Answer part 1: {}'.format(solve_part_one(lines)))


def solve_part_one(lines):
    programs = build_program_tree(lines)

    bottoms = [name for name, data in programs.items() if not data.parent]
    assert len(bottoms) == 1
    return bottoms[0]


def build_program_tree(lines):
    programs = {}
    for line in lines:
        match = re.match('(?P<name>\w+) \((?P<weight>\d+)\)( -> (?P<children>[,\s\w]+))?', line.strip())
        if match:
            name = match.group('name')
            weight = int(match.group('weight'))
            p = programs.setdefault(name, ProgramData())
            p.weight = weight

            if match.groupdict()['children']:
                for child in match.group('children').split(', '):
                    programs.setdefault(child, ProgramData()).parent = name
    return programs


class ProgramData:
    def __init__(self):
        self.weight = None
        self.parent = None

    def __repr__(self) -> str:
        return 'ProgramData(weight={}, parent={})'.format(self.weight, self.parent)


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

assert solve_part_one(test_input.splitlines()) == 'tknk'

if __name__ == '__main__':
    main()
