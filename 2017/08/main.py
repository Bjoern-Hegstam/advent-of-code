import re

REGISTER_DEFAULT_VALUE = 0


def main():
    with open('input') as f:
        lines = f.readlines()

    instructions = parse_instructions(lines)
    largest_value_seen = 0
    current_largest_value = 0

    registers = {}
    for instruction in instructions:
        instruction.execute(registers)
        current_largest_value = max(registers.values()) if registers else 0
        if current_largest_value > largest_value_seen:
            largest_value_seen = current_largest_value

    print('Answer part 1: {}'.format(current_largest_value))
    print('Answer part 2: {}'.format(largest_value_seen))


def solve_part_one(instructions):
    registers = {}
    for instruction in instructions:
        instruction.execute(registers)
    return max(registers.values())


def parse_instructions(lines):
    return [parse_instruction(line) for line in lines]


def parse_instruction(line):
    match = re.match(
        '(?P<op_reg_name>\w+) '
        '(?P<op_type>inc|dec) '
        '(?P<op_val>-?\d+) '
        'if '
        '(?P<cond_reg_name>\w+) '
        '(?P<cond_op>[!><=]+) '
        '(?P<cond_val>-?\d+)',
        line
    )

    if not match:
        raise Exception('Could not parse instruction', line)

    op_reg_name = match.group('op_reg_name')
    op_type = match.group('op_type')
    op_val = int(match.group('op_val'))

    cond_reg_name = match.group('cond_reg_name')
    cond_op = match.group('cond_op')
    cond_val = int(match.group('cond_val'))

    return Instruction(
        Operation(op_reg_name, op_type, op_val),
        Condition(cond_reg_name, cond_op, cond_val)
    )


class Instruction:
    def __init__(self, operation, condition):
        self.operation = operation
        self.condition = condition

    def execute(self, registers):
        if self.condition.check(registers):
            self.operation.execute(registers)

    def __repr__(self):
        return '{} if {}'.format(self.operation, self.condition)


class Operation:
    def __init__(self, register_name, op_type, value):
        self.register_name = register_name
        self.op_type = op_type
        self.value = value

    def execute(self, registers):
        r = registers.get(self.register_name, REGISTER_DEFAULT_VALUE)
        if self.op_type == 'inc':
            r += self.value
        else:
            assert self.op_type == 'dec'
            r -= self.value
        registers[self.register_name] = r

    def __repr__(self):
        return '{} {} {}'.format(self.register_name, self.op_type, self.value)


class Condition:
    def __init__(self, register_name, comparison_operator, comparison_value):
        self.register_name = register_name
        self.comparison_operator = comparison_operator
        self.comparison_value = comparison_value

    def check(self, registers):
        r = registers.get(self.register_name, REGISTER_DEFAULT_VALUE)
        return eval('{} {} {}'.format(r, self.comparison_operator, self.comparison_value))

    def __repr__(self):
        return '{} {} {}'.format(self.register_name, self.comparison_operator, self.comparison_value)


test_input = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""".strip().splitlines()

test_instructions = parse_instructions(test_input)

assert [str(inst) for inst in test_instructions] == test_input
assert solve_part_one(test_instructions) == 1

if __name__ == '__main__':
    main()
