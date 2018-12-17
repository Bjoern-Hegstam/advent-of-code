from util.constants import ALPHABET_LOWER, ALPHABET_UPPER
from util.geometry import Rectangle, Vector2, manhattan_dist, get_bounding_box, get_points, get_nearest_point, pad

alphabet = ALPHABET_LOWER + ALPHABET_UPPER


def main():
    with open('input') as f:
        lines = f.readlines()

    raw_points = [line.split(', ') for line in lines]
    points = [Vector2(int(p[0]), int(p[1])) for p in raw_points]
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


assert get_bounding_box([
    Vector2(1, 1),
    Vector2(1, 6),
    Vector2(8, 3),
    Vector2(3, 4),
    Vector2(5, 5),
    Vector2(8, 9)
]) == Rectangle(1, 1, 8, 9)

assert pad(Rectangle(1, 1, 8, 9), 1) == Rectangle(0, 0, 10, 11)


def print_point_assignments(bounding_box, point_assignments):
    for dy in range(bounding_box.height):
        for dx in range(bounding_box.width):
            p = Vector2(bounding_box.x + dx, bounding_box.y + dy)
            assigned_index = point_assignments[p]
            if assigned_index == -1:
                print('.', end='')
            else:
                print(alphabet[assigned_index], end='')
        print('')


if __name__ == '__main__':
    main()
