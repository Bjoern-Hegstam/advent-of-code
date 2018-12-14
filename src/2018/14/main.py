recipes = [3, 7]
elf_recipe_indices = [0, 1]


def main():
    recipe_threshold = 556061

    recipe_scores = find_recipe_scores(recipe_threshold)
    print('Answer part 1: {}'.format(recipe_scores))


def print_recipe_making():
    assert len(elf_recipe_indices) == 2 # Only have graphics defined for two elves
    for recipe_idx, recipe in enumerate(recipes):
        if recipe_idx == elf_recipe_indices[0]:
            print('({})'.format(recipe), end='')
        elif recipe_idx == elf_recipe_indices[1]:
            print('[{}]'.format(recipe), end='')
        else:
            print(' {} '.format(recipe), end='')
    print('')


def find_recipe_scores(recipe_threshold):
    while len(recipes) < recipe_threshold + 10:
        new_recipe = sum(recipes[elf_recipe_index] for elf_recipe_index in elf_recipe_indices)
        new_scores = [int(c) for c in str(new_recipe)]
        recipes.extend(new_scores)

        for elf_index, elf_recipe_index in enumerate(elf_recipe_indices):
            current_recipe_score = recipes[elf_recipe_index]
            new_recipe_index = (elf_recipe_index + 1 + current_recipe_score) % len(recipes)
            elf_recipe_indices[elf_index] = new_recipe_index

        # print_recipe_making()

    result = ''.join(str(recipe) for recipe in recipes[recipe_threshold:recipe_threshold+10])
    print('Recipe threshold {} gives result: {}'.format(recipe_threshold, result))
    return result


assert find_recipe_scores(5) == '0124515891'
assert find_recipe_scores(9) == '5158916779'
assert find_recipe_scores(18) == '9251071085'
assert find_recipe_scores(2018) == '5941429882'


if __name__ == '__main__':
    main()
