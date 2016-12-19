#!/usr/bin/env python

import fileinput
import argparse

def main(files, part=1):
    input_lines = [line.strip() for line in fileinput.input(files)]
    N = int(input_lines[0])

    if part == 1:
        solve_part_one(N)
    else:
        solve_part_two(N)

def solve_part_one(N):
    # Example
    # 1 2 3 4 5 6 7 8 9 10 | N = 10, n_0 = 1, dn = 1
    # 1   3   5   7   9    | N = 5, n_0 = 1, dn = 2
    #         5       9    | N = 2, n_0 = 5, dn = 4
    #         5            | N = 1, n_0 = 1

    n_0 = 1
    dn = 1
    while N > 1:
        dn *= 2
        if N % 2 != 0:
            n_0 += dn
            N = (N - 1)/ 2
        else:
            N /= 2

    print(n_0)


def solve_part_two(N):
    # Even number
    # 1 2 3 4 5 6 7 8 9 10 | N = 10, 1 -> 0 + N/2 = 5 => 6 goes
    # 1 2 3 4 5   7 8 9 10 | N = 9, 2 -> 1 + (N - 1)/2 = 5 => 7 goes
    # 1 2 3 4 5     8 9 10 | N = 8, 3 -> 2 + N/2 = 6 => 9 goes
    # 1 2 3 4 5     8   10 | N = 7, 4 -> 3 + (N - 1)/2 = 6 => 10 goes

    # 1 2 3 4 5     8      | N = 6, 5 -> 4 + N/2 = 7 = 1 => 2 goes
    #   2 3 4 5     8      | N = 5, 8 -> 5 + (N - 1)/2 = 7 = 2 => 2 goes
    #     3 4 5     8      | N = 4, 3 -> 6 + N/2 = 5 = 1 => 4 goes
    #     3   5     8      | N = 3, 5 -> 7 + (N - 1)/2 = 6 = 0 => 3 goes
    nodes = [Node(i) for i in range(N)]
    for i in range(N):
        nodes[i].next = nodes[(i + 1) % N]
        nodes[i].prev = nodes[(i - 1) % N]

    start = nodes[0]
    mid = nodes[N//2]

    for i in range(N - 1):
        mid.delete()
        mid = mid.next

        if (N - i) % 2 == 1:
            mid = mid.next

        start = start.next

    print(start.id + 1)


class Node:
    def __init__(self, id):
        self.id = id
        self.next = None
        self.prev = None

    def delete(self):
        self.prev.next = self.next
        self.next.prev = self.prev



def seek_to_next_true(nums, start):
    idx = (start + 1) % len(nums)
    while not nums[idx]:
        idx = (idx + 1) % len(nums)
    return idx

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--part', default=1)
    args = parser.parse_args()

    main(args.files, part=args.part)
