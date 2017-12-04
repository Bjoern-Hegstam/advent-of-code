import math
import logging

# Ring index = n
# Side length L = 2*n + 1
# Max number in ring = L^2
# Number of numbers per ring T = 2*L + 2*(L - 2) = 4*n + 2 + 4*n + 2 - 4 = 8*n

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    print('Answer part one: {}'.format(solve_part_one(347991)))


def solve_part_one(val):
    logging.debug('Input val: {}'.format(val))

    if val == 1:
        return 0

    # Find which ring the input is in
    side_length = math.ceil(math.sqrt(val))
    if side_length % 2 == 0:
        side_length += 1

    n = int((side_length - 1) / 2)

    logger.debug('side_length: {}'.format(side_length))
    logger.debug('n: {}'.format(n))

    # Calculate interval and center number for each side
    prev_max_num = (2 * (n - 1) + 1) ** 2
    sides = {
        (prev_max_num + 1, prev_max_num + 2 * n, prev_max_num + n),  # (min num, max num, center)
        (prev_max_num + 2 * n, prev_max_num + 4 * n, prev_max_num + 3 * n),
        (prev_max_num + 4 * n, prev_max_num + 6 * n, prev_max_num + 5 * n),
        (prev_max_num + 6 * n, prev_max_num + 8 * n, prev_max_num + 7 * n)
    }

    logger.debug(prev_max_num)
    logger.debug(sides)

    # Find which side the number is in and calculate distance from center
    dist = -1
    for min_num, max_num, center in sides:
        if min_num <= val <= max_num:
            dist = abs(center - val)
            break
    logger.debug('dist: {}'.format(dist))

    # Add on distance to get to the ring from center in one direction
    dist += n
    logger.debug('Total dist: {}'.format(dist))
    return dist


assert solve_part_one(1) == 0
assert solve_part_one(12) == 3
assert solve_part_one(23) == 2
assert solve_part_one(1024) == 31


if __name__ == '__main__':
    main()
