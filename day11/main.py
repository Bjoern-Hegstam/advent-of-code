#!/usr/bin/env python

import fileinput
import re
import time

from collections import deque

class State:
    def __init__(self, floor_count, components=None, elevator=1):
        self.__floor_count = floor_count
        self.__components = components if components else {}
        self.__elevator = elevator

    def copy(self):
        return State(self.__floor_count, dict(self.__components), self.__elevator)

    def is_same_state(self, other_state):
        return self.__floor_count == other_state.__floor_count and \
                self.__components == other_state.__components and \
                self.__elevator == other_state.__elevator

    def add(self, component, floor):
        self.__components[component] = floor

    def generate_next_states(self):
        possible_payloads = []

        components = self.__get_components_by_floor()[self.__elevator]
        for idx, c in enumerate(components):
            possible_payloads.append([c])

            for c2 in components[idx+1:]:
                possible_payloads.append([c, c2])

        possible_directions = []
        if self.__elevator < self.__floor_count:
            possible_directions.append(1)

        if self.__elevator > 1:
            possible_directions.append(-1)

        moves = [Move(direction, payload) for payload in possible_payloads for direction in possible_directions]
        res = []

        for move in moves:
            new_state = self.copy()
            new_state.do_move(move)
            if new_state.is_valid():
                res.append((move, new_state))

        return res

    def do_move(self, move):
        self.__elevator += move.direction
        for c in move.components:
            self.__components[c] = self.__components[c] + move.direction

    def is_valid(self):
        for floor, components in self.__get_components_by_floor().items():
            # Safe if floor has no chips
            if not components:
                continue

            # Auto-safe if there are no generators
            if not any(c[1] == 'G' for c in components):
                continue

            # Otherwise, ensure each microchip has a corresponding RTG
            for c in components:
                if c[1] == 'G':
                    continue

                required_rtg = c[0] + 'G'
                if self.__components[required_rtg] != floor:
                    return False

        return True

    def is_final_state(self):
        components_by_floor = self.__get_components_by_floor()

        return len(components_by_floor) == 1 and self.__floor_count in components_by_floor

    def __get_components_by_floor(self):
        components_by_floor = {}
        for c, floor in self.__components.items():
            components_by_floor.setdefault(floor, []).append(c)
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
    def __init__(self, state, parent_node=None):
        self.state = state
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

    node_queue = deque()
    node_queue.append(Node(initial_state))

    visited_states = []

    while node_queue:
        parent_node = node_queue.popleft()
        visited_states.append(parent_node.state)

        #print(len(node_queue))
        #print(parent_node.state, flush=True)
        #time.sleep(0.5)

        if parent_node.state.is_final_state():
            step_count = 0
            temp_node = parent_node
            while temp_node.parent_node:
                temp_node = temp_node.parent_node
                step_count += 1

            print(parent_node.state)
            print(str(step_count))
            break

        for move, state in parent_node.state.generate_next_states():
            skip = False
            for visited in visited_states:
                if state.is_same_state(visited):
                    skip = True
                    break

            if skip:
                continue

            node_queue.append(Node(state, parent_node))


if __name__ == '__main__':
    main()
