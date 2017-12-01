#!/usr/bin/env python

import fileinput
import argparse

class Register:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def set(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

def print_registers(registers):
    for name, register in sorted(registers.items()):
        print('%s - %s' % (name, register))

def get_value(registers, name_or_value):
    if name_or_value in registers:
        return registers[name_or_value].value
    return int(name_or_value)

def main(part, files):
    registers = {
        'a': Register(),
        'b': Register(),
        'c': Register(),
        'd': Register()
    }

    lines = [line.strip() for line in fileinput.input(files)]

    if part == 2:
        registers['c'].value = 1

    idx = 0
    while idx < len(lines):
        inst = lines[idx].split()
        if inst[0] == 'inc':
            registers[inst[1]].increment()
            idx += 1
        elif inst[0] == 'dec':
            registers[inst[1]].decrement()
            idx += 1
        elif inst[0] == 'cpy':
            registers[inst[2]].value = get_value(registers, inst[1])
            idx += 1
        elif inst[0] == 'jnz':
            if get_value(registers, inst[1]) != 0:
                idx += int(inst[2])
            else:
                idx += 1

    print('---')
    print_registers(registers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', default='1', type=int)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    main(args.part, args.files)
