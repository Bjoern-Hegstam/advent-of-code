INITIAL_RECIPES = [3, 7]
INITIAL_ELF_RECIPE_INDICES = [0, 1]


def main():
    recipe_threshold = 556061

    recipe_scores = find_recipe_scores(recipe_threshold)
    print('Answer part 1: {}'.format(recipe_scores))

    recipe_count = get_recipe_count_before(str(recipe_threshold))
    print('Answer part 2: {}'.format(recipe_count))


def print_recipe_making(recipes, elf_recipe_indices):
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
    recipes = INITIAL_RECIPES.copy()
    elf_recipe_indices = INITIAL_ELF_RECIPE_INDICES.copy()

    while len(recipes) < recipe_threshold + 10:
        make_next_recipe(recipes, elf_recipe_indices)

    result = ''.join(str(recipe) for recipe in recipes[recipe_threshold:recipe_threshold+10])
    print('find_recipe_scores: Recipe threshold {} gives result {}'.format(recipe_threshold, result))
    return result


def make_next_recipe(recipes, elf_recipe_indices):
    new_recipe = sum(recipes[elf_recipe_index] for elf_recipe_index in elf_recipe_indices)
    new_scores = [int(c) for c in str(new_recipe)]
    recipes.extend(new_scores)

    for elf_index, elf_recipe_index in enumerate(elf_recipe_indices):
        current_recipe_score = recipes[elf_recipe_index]
        new_recipe_index = (elf_recipe_index + 1 + current_recipe_score) % len(recipes)
        elf_recipe_indices[elf_index] = new_recipe_index


assert find_recipe_scores(5) == '0124515891'
assert find_recipe_scores(9) == '5158916779'
assert find_recipe_scores(18) == '9251071085'
assert find_recipe_scores(2018) == '5941429882'


def get_recipe_count_before(recipe_str_pattern):
    recipe_pattern = [int(c) for c in recipe_str_pattern]
    pattern_search_idx = 0

    recipes = INITIAL_RECIPES.copy()
    elf_recipe_indices = INITIAL_ELF_RECIPE_INDICES.copy()

    recipe_count = len(recipes)

    while True:
        make_next_recipe(recipes, elf_recipe_indices)
        recipe_count += 1

        if recipe_count % 100000 == 0:
            print('get_recipe_count_before: recipe_count={}'.format(recipe_count))

        while pattern_search_idx < len(recipes) - len(recipe_pattern) + 1:
            found_pattern = True
            for idx, i in enumerate(recipe_pattern):
                if recipes[pattern_search_idx + idx] != recipe_pattern[idx]:
                    pattern_search_idx += 1
                    found_pattern = False
                    break
            if found_pattern:
                result = pattern_search_idx
                print('get_recipe_count_before: Input {} gives result {}'.format(recipe_str_pattern, result))
                return result


assert get_recipe_count_before('01245') == 5
assert get_recipe_count_before('51589') == 9
assert get_recipe_count_before('92510') == 18
assert get_recipe_count_before('59414') == 2018


if __name__ == '__main__':
    main()
