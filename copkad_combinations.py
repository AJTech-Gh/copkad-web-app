import itertools

def get_valid_combinations():
    # define ministries dictionary
    ministries = {'C': 'Children', 'E': 'Evangelism', 'P': 'Pemem', 'W': 'Women', 'Y': 'Youth'}
    exceptions = ['CW', 'CY']
    # get all the combinations of at most 3 ministries
    all_combinations = set()
    for r in range(1, 4):
        all_combinations.update(itertools.combinations(ministries.keys(), r))
    # sort the combinations
    all_combinations = [tuple(sorted(m)) for m in all_combinations]
    # remove the incompatible departments
    found_exceptions = set()
    for c in all_combinations:
        for e in exceptions:
            if all([any([c.__contains__(v), c == e]) for v in list(e)]):
                found_exceptions.add(c)
    for e in found_exceptions:
        all_combinations.remove(e)
    # join all combinations into strings
    all_combinations = [''.join(m) for m in all_combinations]
    return all_combinations

print(len(get_valid_combinations()))
