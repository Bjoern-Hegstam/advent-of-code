#!/usr/bin/env python

import fileinput
import re
import time
import itertools

from collections import deque

def log(s):
    print(s)
    #pass

def get_component_type(component):
    return component[1]

def get_component_name(component):
    return component[0]

def is_microchip(component):
    return get_component_type(component) == ComponentType.MICROCHIP

def is_generator(component):
    return get_component_type(component) == ComponentType.GENERATOR

def get_generator(microchip):
    return get_component_name(microchip) + ComponentType.GENERATOR

def get_microchip(generator):
    return get_component_name(generator) + ComponentType.MICROCHIP

class State:
    def __init__(self, floor_count, components=None, elevator=1):
        self.__floor_count = floor_count
        self.__components = components if components else {}
        self.__components_by_floor = self.__get_components_by_floor()
        self.__elevator = elevator

    def copy(self):
        return State(self.__floor_count, dict(self.__components), self.__elevator)

    def add(self, component, floor):
        self.__components[component] = floor
        self.__components_by_floor = self.__get_components_by_floor()

    def generate_next_states(self):
        possible_directions = []
        if self.__elevator < self.__floor_count:
            possible_directions.append(1)

        if self.__elevator > 1:
            possible_directions.append(-1)

        moves = []
        current_floor_components = self.__components_by_floor[self.__elevator]
        for d, c1, c2 in itertools.product(possible_directions, current_floor_components, current_floor_components):
            if c1 == c2:
                moves.append(Move(d, [c1]))
            else:
                moves.append(Move(d, [c1, c2]))

        seen_states = []

        res = []
        for move in moves:
            new_state = self.copy()
            new_state.do_move(move)
            if new_state.is_valid() and new_state.__repr__() not in seen_states:
                res.append((move, new_state))
                seen_states.append(new_state.__repr__())
        return res

    def is_valid(self):
        for floor, components in self.__components_by_floor.items():
            # Safe if floor has no components
            if not components:
                continue

            # No generators on floor
            if not self.__floor_has_generators(floor):
                continue

            # Otherwise, ensure each microchip has a corresponding RTG
            for c in components:
                if is_generator(c):
                    continue

                if not get_generator(c) in components:
                    return False

        return True

    def __floor_has_generators(self, floor):
        for c in self.__components_by_floor[floor]:
            if is_generator(c):
                return True
        return False

    def do_move(self, move):
        self.__elevator += move.direction
        for c in move.components:
            self.__components[c] = self.__components[c] + move.direction
        self.__components_by_floor = self.__get_components_by_floor()

    def is_final_state(self):
        floor_with_components_count = 0
        for floor, components in self.__components_by_floor.items():
            if components and not floor == self.__floor_count:
                return False

        return True

    def __get_components_by_floor(self):
        components_by_floor = {}
        for c, floor in self.__components.items():
            components_by_floor.setdefault(floor, []).append(c)

        for floor in range(1, self.__floor_count + 1):
            components_by_floor.setdefault(floor, [])

        return components_by_floor


    def __repr__(self):
        res = ''
        for floor in range(self.__floor_count, 0, -1):
            res += 'F' + str(floor).zfill(len(str(self.__floor_count)))
            res += ' '
            res += 'E' if self.__elevator == floor else '.'
            res += ' '
            
            for c, c_floor in sorted(self.__components.items()):
                res += c if c_floor == floor else '. '
                res += ' '

            res += '\n'
        return res

class Move:
    def __init__(self, direction, components):
        self.direction = direction
        self.components = components

    def __repr__(self):
        return '%s - %s' % (self.direction, self.components)

class ComponentType:
    GENERATOR = 'G'
    MICROCHIP = 'M'

class Node:
    def __init__(self, state, move=None, parent_node=None):
        self.state = state
        self.move = move
        self.parent_node = parent_node

def main():
    initial_state = State(4)

    element_to_letter = {
         'lithium': 'L',
         'lithium-compatible': 'L',

         'hydrogen': 'H',
         'hydrogen-compatible': 'H',

         'strontium': 'S',
         'strontium-compatible': 'S',

         'plutonium' : 'P',
         'plutonium-compatible' : 'P',

         'thulium': 'T',
         'thulium-compatible': 'T',

         'ruthenium': 'R',
         'ruthenium-compatible': 'R',

         'curium': 'C',
         'curium-compatible': 'C',

         'cobalt': 'N',
         'cobalt-compatible': 'N',

         'promethium': 'Q',
         'promethium-compatible': 'Q'
    }

    component_type_to_letter = {
        'generator': ComponentType.GENERATOR,
        'microchip': ComponentType.MICROCHIP
    }

    floor_name_to_number = {
        'first': 1,
        'second': 2,
        'third': 3,
        'fourth': 4
    }

    for line in fileinput.input():
        if 'nothing relevant' in line:
            continue

        line_parts = re.split(r', | |\.', line.strip())
        floor = floor_name_to_number[line_parts[1]]

        for idx, line_part in enumerate(line_parts):
            if line_part in component_type_to_letter:
                component = element_to_letter[line_parts[idx - 1]] + component_type_to_letter[line_part]
                initial_state.add(component, floor)

    #initial_state = State(4, elevator=3)
    #initial_state.add('HG', 4)
    #initial_state.add('HM', 3)
    #initial_state.add('LG', 4)
    #initial_state.add('LM', 3)

    node_queue = deque()
    node_queue.append(Node(initial_state))

    visited_states = []

    print(initial_state)

    final_node = None
    while node_queue:
        parent_node = node_queue.popleft()

        if parent_node.state.__repr__() in visited_states:
            continue

        visited_states.append(parent_node.state.__repr__())

        print(len(visited_states))
        print(len(unwind_path(parent_node)), flush=True)

        #print('Checking state')
        #print(parent_node.state)
        #print('Is final: %s' % parent_node.state.is_final_state(), flush=True)
        #time.sleep(1)

        if parent_node.state.is_final_state():
            final_node = parent_node
            break

        for move, state in parent_node.state.generate_next_states():
            if not state.__repr__() in visited_states:
                node_queue.append(Node(state, move, parent_node))

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
