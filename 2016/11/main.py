#!/usr/bin/env python

import fileinput
import re
import time
import itertools

from collections import deque

#Initial state
#F4 . .  .  .  .  .  .  .  .  .  .
#F3 . .  .  .  .  .  .  .  .  .  TM
#F2 . CG CM .  .  RG RM .  .  TG .
#F1 E .  .  PG PM .  .  SG SM .  .

COMPONENTS = ['HG', 'HM', 'LG', 'LM']
COMPONENTS = ['CG', 'CM', 'PG', 'PM', 'RG', 'RM', 'SG', 'SM', 'TG', 'TM']
COMPONENTS = ['CG', 'CM', 'PG', 'PM', 'RG', 'RM', 'SG', 'SM', 'TG', 'TM', 'EG', 'EM', 'DG', 'DM']

def log(s):
    print(s)

class ComponentType:
    GENERATOR = 'G'
    MICROCHIP = 'M'

class Component:
    def __init__(self, name, component_type):
        self.name = name
        self.type = component_type

    def __repr__(self):
        return '%s%s' % (self.name, self.type)

class State:
    def __init__(self, floor_count, components, elevator=1):
        self.__floor_count = floor_count
        self.__components = components
        self.__elevator = elevator

    def copy(self):
        return State(self.__floor_count, list(self.__components), self.__elevator)

    def generate_next_states(self):
        possible_directions = []
        if self.__elevator < self.__floor_count:
            possible_directions.append(1)

        if self.__elevator > 1:
            possible_directions.append(-1)

        components_indices_on_floor = [idx for idx, floor in enumerate(self.__components) if floor == self.__elevator]
        for d, idx1, idx2 in itertools.product(possible_directions, components_indices_on_floor, components_indices_on_floor):
            new_components = list(self.__components)
            new_components[idx1] += d
            if idx1 != idx2:
                new_components[idx2] += d

            new_state = State(self.__floor_count, new_components, self.__elevator + d)
            if new_state.__is_valid():
                yield (Move(d), new_state)

    def __is_valid(self):
        generator_floors = self.__components[::2]
        for idx, chip_floor in enumerate(self.__components):
            if idx % 2 == 0:
                # Generator
                continue

            if chip_floor in generator_floors and not self.__components[idx - 1] == chip_floor:
                return False

        return True

    def is_final_state(self):
        return all(c == self.__floor_count for c in self.__components)

    def hash(self):
        component_pairs = list(zip(self.__components[::2], self.__components[1::2]))
        return {'e': self.__elevator, 'c': sorted(component_pairs)}

    def __repr__(self):
        res = ''
        for floor in range(self.__floor_count, 0, -1):
            res += 'F' + str(floor).zfill(len(str(self.__floor_count)))
            res += ' '
            res += 'E' if self.__elevator == floor else '.'
            res += ' '
            
            for idx, f in enumerate(self.__components):
                res += COMPONENTS[idx] if f == floor else '. '
                res += ' '

            res += '\n'
        return res

class Move:
    def __init__(self, direction):
        self.direction = direction

    def __repr__(self):
        return '%s' % (self.direction)

class Node:
    def __init__(self, state, move=None, parent_node=None):
        self.state = state
        self.move = move
        self.parent_node = parent_node

def main():
    floor_count = 4
    components = [3, 3, 1, 2, 3, 3, 1, 2, 1, 1]
    components = [2, 1, 3, 1]
    components = [2, 2, 1, 1, 2, 2, 1, 1, 2, 3]
    components = [2, 2, 1, 1, 2, 2, 1, 1, 2, 3, 1, 1, 1, 1]
    elevator = 1

    initial_state = State(floor_count, components, elevator)
    print(initial_state)

    node_queue = deque()
    node_queue.append(Node(initial_state))

    visited_states = []
    visited_states.append(initial_state.hash())

    final_node = None
    counter = 0
    while node_queue:
        counter += 1
        if counter % 1000 == 0:
            print('%s: Queue size: %s' % (counter, len(node_queue)), flush=True)

        parent_node = node_queue.popleft()

        if parent_node.state.is_final_state():
            final_node = parent_node
            break

        for move, state in parent_node.state.generate_next_states():
            if not state.hash() in visited_states:
                node_queue.append(Node(state, move, parent_node))
                visited_states.append(state.hash())

    if final_node:
        step_count = 0
        node_path = []
        node_path.append(final_node)
        
        temp_node = parent_node
        while temp_node.parent_node:
            temp_node = temp_node.parent_node
            step_count += 1
            node_path.append(temp_node)

        for node in reversed(node_path):
            log(node.move)
            log(node.state)

        log(len(node_path) - 1)


def unwind_path(end_node):
    node_path = []
    node_path.append(end_node)
    
    temp_node = end_node
    while temp_node.parent_node:
        temp_node = temp_node.parent_node
        node_path.append(temp_node)
    return node_path

if __name__ == '__main__':
    main()
