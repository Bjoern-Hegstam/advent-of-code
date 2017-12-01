#!/usr/bin/env python

import fileinput

from collections import deque

class Bot:
    def __init__(self, bot_id):
        self.__bot_id = bot_id
        self.__values = []
        self.__instruction_queue = deque()

    def give_chip(self, value):
        self.__values.append(value)
        self.__values.sort()

        self.__try_execute_next_instruction()

    def add_instruction(self, instruction):
        self.__instruction_queue.append(instruction)
        self.__try_execute_next_instruction()

    def __try_execute_next_instruction(self):
        if len(self.__values) < 2:
            return

        if not self.__instruction_queue:
            return

        print('Bot %s - %s' % (self.__bot_id, self.__values))

        instr = self.__instruction_queue.popleft()
        instr.low_target_fun(self.__values[0])
        instr.high_target_fun(self.__values[1])
        self.__values = []

    def __repr__(self):
        return '%s - %s' % (self.__bot_id, self.__values)

class BotInstruction:
    def __init__(self, low_target_fun, high_target_fun):
        self.low_target_fun = low_target_fun
        self.high_target_fun = high_target_fun

def get_target_fun(bots, outputs, target_type, target_idx):
    if target_type == 'bot':
        return bots.setdefault(target_idx, Bot(target_idx)).give_chip
    else:
        return outputs.setdefault(target_idx, []).append

def main():
    bots = {}
    outputs = {}

    for line in fileinput.input():
        instruction = line.strip().split()
        if instruction[0] == 'value':
            value = int(instruction[1])
            bot_idx = instruction[-1]
            bots.setdefault(bot_idx, Bot(bot_idx)).give_chip(value)
        else:
            bot_idx = instruction[1]
            targets = {}
            targets[instruction[3]] = get_target_fun(bots, outputs, instruction[5], instruction[6])
            targets[instruction[8]] = get_target_fun(bots, outputs, instruction[10], instruction[11])
            bots.setdefault(bot_idx, Bot(bot_idx)).add_instruction(BotInstruction(targets['low'], targets['high']))

    print('---')
    print('Outputs')
    for output_id in sorted(outputs):
        print('%s - %s' % (output_id, outputs[output_id]))

    print('---')
    product = 1
    for idx in range(3):
        product *= int(outputs[str(idx)][0])
    print('Part 2: %s' % product)



if __name__ == '__main__':
    main()
