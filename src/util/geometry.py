from collections import namedtuple

Rectangle = namedtuple('Rectangle', 'x, y, width, height')
Point = namedtuple('Point', 'x, y')


def manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)
