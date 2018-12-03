import re

from collections import namedtuple


Claim = namedtuple('Claim', 'id, x, y, width, height')
claim_pattern = re.compile(r'^#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<width>\d+)x(?P<height>\d+)$')


def main():
    with open('input') as f:
        lines = f.readlines()

    claims = [parse_claim(line.strip()) for line in lines]

    overlap_count, unoverlapping_claim_ids = calc_overlap(claims)
    print('Answer part 1: {}'.format(overlap_count))
    print('Answer part 2: {}'.format(unoverlapping_claim_ids))


def parse_claim(claim_str):
    match = claim_pattern.match(claim_str)
    assert match
    return Claim(
        int(match.group('id')),
        int(match.group('x')),
        int(match.group('y')),
        int(match.group('width')),
        int(match.group('height')),
    )


assert parse_claim('#934 @ 370,555: 18x14') == Claim(934, 370, 555, 18, 14)


def calc_overlap(claims):
    fabric_use_count = {}
    overlapping_claim_ids = set()

    for claim in claims:
        for x, y in gen_claim_coordinates(claim):
            claim_ids = fabric_use_count.setdefault((x, y), [])
            if len(claim_ids) > 0:
                overlapping_claim_ids.add(claim.id)
                for cid in claim_ids:
                    overlapping_claim_ids.add(cid)

            claim_ids.append(claim.id)

    overlap_count = len([k for k, v in fabric_use_count.items() if len(v) > 1])
    unoverlapping_claim_ids = [claim.id for claim in claims if claim.id not in overlapping_claim_ids]

    return overlap_count, unoverlapping_claim_ids


def gen_claim_coordinates(claim):
    for dx in range(claim.width):
        for dy in range(claim.height):
            x = claim.x + dx
            y = claim.y + dy
            yield x, y


assert calc_overlap([
    Claim(1, 1, 3, 4, 4),
    Claim(2, 3, 1, 4, 4),
    Claim(3, 5, 5, 2, 2),
])[0] == 4, [3]


if __name__ == '__main__':
    main()
