def main():
    with open('input') as f:
        lines = f.readlines()

    words = [line.strip() for line in lines]

    print('Answer part 1: {}'.format(calc_checksum(words)))
    print('Answer part 2: {}'.format(find_common_letters_of_correct_box_ids(words)))


def calc_checksum(words):
    two_count = 0
    three_count = 0
    for word in words:
        letter_counts = get_word_letter_counts(word)
        if 2 in letter_counts:
            two_count += 1
        if 3 in letter_counts:
            three_count += 1

    return two_count * three_count


def get_word_letter_counts(word):
    histogram = {}

    for letter in word:
        histogram[letter] = 1 + histogram.get(letter, 0)

    return histogram.values()


def find_common_letters_of_correct_box_ids(words):
    for w1 in words[:-1]:
        for w2 in words[1:]:
            common_letters = []
            diff_count = 0
            for i in range(len(w1)):
                if w1[i] == w2[i]:
                    common_letters.append(w1[i])
                else:
                    diff_count += 1
            if diff_count == 1:
                print('w1: {}'.format(w1))
                print('w2: {}'.format(w2))
                return ''.join(common_letters)


if __name__ == '__main__':
    main()
