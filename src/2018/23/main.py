import re
from collections import namedtuple

from util.geometry import Vector3, manhattan_dist

input_pattern = re.compile(r'pos=<(?P<p_x>-?\d+),(?P<p_y>-?\d+),(?P<p_z>-?\d+)>, r=(?P<r>\d+)')

Bot = namedtuple('Bot', 'position, radius')


def main():
    bots = load_bots('input')

    max_radius_bot = max(bots, key=lambda b: b.radius)
    bots_in_radius = [bot for bot in bots if manhattan_dist(max_radius_bot.position, bot.position) <= max_radius_bot.radius]
    print('Answer part 1: {}'.format(len(bots_in_radius)))


def load_bots(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    bots = []
    for line in lines:
        match = input_pattern.match(line)
        assert match

        bots.append(Bot(
            Vector3(
                int(match.group('p_x')),
                int(match.group('p_y')),
                int(match.group('p_z'))
            ),
            int(match.group('r'))
        ))

    return bots


if __name__ == '__main__':
    main()
