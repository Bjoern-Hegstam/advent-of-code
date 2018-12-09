DEBUG = False


def main():
    player_count = 438
    marble_count = 71626

    high_score = play_marble_game(player_count, marble_count)
    print('Answer part 1: {}'.format(high_score))


def play_marble_game(player_count, marble_count):
    marbles = [0]
    next_marble = 1
    current_marble_idx = 0
    scores = {}

    print('Playing game: {} players, {} marbles'.format(player_count, marble_count))

    player_idx = 0
    while next_marble <= marble_count:
        if DEBUG:
            print('Current marble is {} at index {}, next marble is {}'.format(marbles[current_marble_idx], current_marble_idx, next_marble))

        if next_marble % 23 == 0:
            next_marble_idx = (current_marble_idx - 7) % len(marbles)
            marble_to_delete = marbles[next_marble_idx]

            if DEBUG:
                print('Found multiple of 23: {}, deleting marble {} at index {}'.format(next_marble, marble_to_delete, next_marble_idx))

            scores[player_idx] = scores.get(player_idx, 0) + next_marble + marble_to_delete
            del marbles[next_marble_idx]
            current_marble_idx = next_marble_idx
        else:
            next_marble_idx = current_marble_idx + 2
            if next_marble_idx == len(marbles) + 1:
                next_marble_idx = 1

            if DEBUG:
                print('Adding marble {} at index {}'.format(next_marble, next_marble_idx))

            marbles.insert(next_marble_idx, next_marble)
            current_marble_idx = next_marble_idx

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
