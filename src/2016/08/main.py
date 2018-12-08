#!/usr/bin/env python

import fileinput

class PixelState:
    ON = '#'
    OFF = ' '

WIDTH = 50
HEIGHT = 6

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__display = [[PixelState.OFF] * width for x in range(height)]
        self.__buffer = [[PixelState.OFF] * width for x in range(height)]

    def fill_rect(self, width, height):
        for y in range(height):
            for x in range(width):
                self.__buffer[y][x] = PixelState.ON
        self._write_buffer_to_display()

    def rotate_row(self, row, n):
        for col in range(self.width):
            self.__buffer[row][col] = self.__display[row][(col - n) % self.width]

        self._write_buffer_to_display()

    def rotate_column(self, col, n):
        for row in range(self.height):
            self.__buffer[row][col] = self.__display[(row - n) % self.height][col]

        self._write_buffer_to_display()

    def lit_count(self):
        return self.__repr__().count(PixelState.ON)

    def _write_buffer_to_display(self):
        for row in range(self.height):
            for col in range(self.width):
                self.__display[row][col] = self.__buffer[row][col]

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.__display])

display = Display(WIDTH, HEIGHT)

for line in fileinput.input():
    cmd_parts = line.strip().split()
    if cmd_parts[0] == 'rect':
        dim = cmd_parts[1].split('x')
        display.fill_rect(int(dim[0]), int(dim[1]))

    if cmd_parts[0] == 'rotate':
        dim = int(cmd_parts[2][2:])
        n = int(cmd_parts[-1])
        if cmd_parts[1] == 'row':
            display.rotate_row(dim, n)
        else:
            display.rotate_column(dim, n)

print(display)
print('Lit count: %s' % display.lit_count())