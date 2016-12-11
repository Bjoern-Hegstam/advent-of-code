#!/usr/bin/env python

import fileinput
import re

class State:
    def __init__(self, floor_count, components=None):
        self.__floor_count = floor_count
        self.__components = components if components else {}
        self.__elevator = 1

    def copy(self):
        return State(self.__floor_count, dict(self.__components))

    def add(self, component, floor):
        self.__components[component] = floor

    def do_move(self, move):
        self.__elevator += move.direction
        for c in move.components:
            self.__components[c] = self.__components[c] + move.direction

    def is_valid(self):
        for floor, components in self.__get_components_by_floor().items():
            # Safe if floor has no chips
            if not components:
                return True

            # Otherwise, ensure each microchip has a corresponding RTG
            for c in components:
                if c[1] == 'G':
                    continue

                required_rtg = c[0] + 'G'
                if self.__components[required_rtg] != floor:
                    return False

        return True

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

def main():
    initial_state = State(4)

    element_to_letter = {
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
        'generator': 'G',
        'microchip': 'M'
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


    print(initial_state)

    # TODO: Run bfs to find state where all chips and RGTs are on the top floor

if __name__ == '__main__':
    main()
