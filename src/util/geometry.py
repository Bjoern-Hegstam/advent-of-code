import math
from collections import namedtuple

Rectangle = namedtuple('Rectangle', 'x, y, width, height')
Vector2 = namedtuple('Vector2', 'x, y')


def manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_bounding_box(points):
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    return Rectangle(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)


def get_points(rect):
    for dy in range(rect.height):
        for dx in range(rect.width):
            yield Vector2(rect.x + dx, rect.y + dy)


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