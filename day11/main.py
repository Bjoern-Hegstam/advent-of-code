#!/usr/bin/env python

import fileinput


class State:
    def __init__(self, components=None):
        self.__components = components if components else {}
        self.__elevator = 1

    def copy(self):
        return State(dict(self.__components))

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
        top_floor = max(self.__components.values())

        res = ''
        for floor in range(top_floor, 0, -1):
            res += 'F' + str(floor).zfill(len(str(top_floor)))
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
    initial_state = State()

    for line in fileinput.input():
        # TODO: Construct initial state
        pass
    initial_state.add('HG', 3)
    initial_state.add('HM', 2)
    initial_state.add('LG', 20)

    print(initial_state)

    # TODO: Run bfs to find state where all chips and RGTs are on the top floor

if __name__ == '__main__':
    main()
