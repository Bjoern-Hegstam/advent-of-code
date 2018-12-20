import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return 31 * self.x + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __repr__(self):
        return 'Vector2(x={}, y={})'.format(self.x, self.y)


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def pad(self, size):
        return Rectangle(self.x - size, self.y - size, self.width + 2 * size, self.height + 2 * size)

    def get_points(self):
        for dy in range(self.height):
            for dx in range(self.width):
                yield Vector2(self.x + dx, self.y + dy)

    def contains(self, p):
        return self.x <= p.x < self.x + self.width and self.y <= p.y < self.y + self.height

    def __hash__(self):
        h = 31 * self.x
        h += 31 * self.y
        h += 31 * self.width
        h += 31 * self.height
        return h

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def __repr__(self):
        return 'Rectangle(x={}, y={}, width={}, height={})'.format(self.x, self.y, self.width, self.height)


def manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_bounding_box(points):
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    return Rectangle(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)


def get_nearest_point(points, target, dist_fun):
    distances = [dist_fun(p, target) for p in points]
    min_dist = math.inf
    min_dist_indices = []
    for idx, dist in enumerate(distances):
        if dist < min_dist:
            min_dist = dist
            min_dist_indices = [idx]
        elif dist == min_dist:
            min_dist_indices.append(idx)

    if len(min_dist_indices) > 1:
        return -1
    else:
        return min_dist_indices[0]


class Direction:
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
