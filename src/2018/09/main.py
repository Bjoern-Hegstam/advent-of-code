from collections import deque


def main():
    high_score_part_one = play_marble_game(438, 71626)
    assert high_score_part_one == 398730
    print('Answer part 1: {}'.format(high_score_part_one))

    high_score_part_two = play_marble_game(438, 7162600)
    assert high_score_part_two == 3349635509
    print('Answer part 2: {}'.format(high_score_part_two))


def play_marble_game(player_count, marble_count):
    marbles = deque()
    marbles.append(0)
    next_marble = 1
    scores = {}

    print('Playing game: {} players, {} marbles'.format(player_count, marble_count))

    player_idx = 0
    while next_marble <= marble_count:
        if next_marble % 23 == 0:
            marbles.rotate(-7)
            scores[player_idx] = scores.get(player_idx, 0) + next_marble + marbles.pop()
        else:
            marbles.rotate(2)
            marbles.append(next_marble)

        player_idx = (player_idx + 1) % player_count
        next_marble += 1

    print('Scores: {}'.format(scores))
    print('')
    return max(scores.values())


assert play_marble_game(9, 25) == 32
assert play_marble_game(10, 1618) == 8317
assert play_marble_game(13, 7999) == 146373
assert play_marble_game(17, 1104) == 2764
assert play_marble_game(21, 6111) == 54718
assert play_marble_game(30, 5807) == 37305

if __name__ == '__main__':
    main()
