import math
from collections import namedtuple

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

Point = namedtuple('Point', 'x, y')
Rectangle = namedtuple('Rectangle', 'x, y, width, height')


def main():
    with open('input') as f:
        lines = f.readlines()

    raw_points = [line.split(', ') for line in lines]
    points = [Point(int(p[0]), int(p[1])) for p in raw_points]
    bounding_box = pad(get_bounding_box(points), 1)

    area_counts = find_bounded_area_sizes(points, bounding_box)
    print('Answer part 1: {}'.format(max(area_counts.values())))

    region_size = len([target for target in get_points(bounding_box) if sum([manhattan_dist(p, target) for p in points]) < 1e4])
    print('Answer part 2: {}'.format(region_size))


def find_bounded_area_sizes(points, bounding_box):
    point_assignments = {}
    for p in get_points(bounding_box):
        nearest_point = get_nearest_point(points, p, manhattan_dist)
        point_assignments[p] = nearest_point

    # Start with all points allowed
    bounded_area_sizes = dict(zip(range(len(points)), [0] * len(points)))

    # Trim away any point on an edge
    for p, idx in point_assignments.items():
        if idx not in bounded_area_sizes:
            continue
        if p.x == bounding_box.x or p.y == bounding_box.y or p.x == (bounding_box.x + bounding_box.width - 1) or p.y == (bounding_box.y + bounding_box.height - 1):
            del bounded_area_sizes[idx]
        else:
            bounded_area_sizes[idx] += 1

    return bounded_area_sizes


def get_bounding_box(points):
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    return Rectangle(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)


assert get_bounding_box([
    Point(1, 1),
    Point(1, 6),
    Point(8, 3),
    Point(3, 4),
    Point(5, 5),
    Point(8, 9)
]) == Rectangle(1, 1, 8, 9)


def pad(rect, size):
    return Rectangle(rect.x - size, rect.y - size, rect.width + 2 * size, rect.height + 2 * size)


assert pad(Rectangle(1, 1, 8, 9), 1) == Rectangle(0, 0, 10, 11)


def get_points(rect):
    for dy in range(rect.height):
        for dx in range(rect.width):
            yield Point(rect.x + dx, rect.y + dy)


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


def manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def print_point_assignments(bounding_box, point_assignments):
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            p = Point(bounding_box.x + dx, bounding_box.y + dy)
            assigned_index = point_assignments[p]
            if assigned_index == -1:
                print('.', end='')
            else:
                print(alphabet[assigned_index], end='')
        print('')


if __name__ == '__main__':
    main()
