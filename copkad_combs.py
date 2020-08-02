import itertools

class MinistryCodeGen():

    def __init__(self):
        # define the maximum length of the ministries code
        self.max_mininstry_code_len = 2
        # define ministries dictionary
        self.ministries = {'C': 'Children', 'E': 'Evangelism', 'P': 'Pemem', 'W': 'Women', 'Y': 'Youth'}
        # define the exceptions list. This list holds all the incompatible combinations of ministries
        self.exceptions = ['CE', 'CP', 'CW', 'CY', 'PW']

    def get_valid_ministry_combs(self):
        """
        Returns all the valid ministry combinations
        """
        all_ministry_combs = set()
        # get all the combinations of at most 3 ministries
        for r in range(1, 4):
            all_ministry_combs.update(itertools.combinations(self.ministries.keys(), r))
        # sort the combinations
        all_ministry_combs = [tuple(sorted(m)) for m in all_ministry_combs]
        # remove the incompatible departments
        found_exceptions = set()
        for c in all_ministry_combs:
            for e in self.exceptions:
                if all([any([c.__contains__(v), c == e]) for v in list(e)]):
                    found_exceptions.add(c)
        for e in found_exceptions:
            all_ministry_combs.remove(e)
        # join all combinations into strings
        all_ministry_combs = sorted([''.join(m) for m in all_ministry_combs])
        # return all the valid combinations
        return all_ministry_combs

    def get_ministry_combs_with_code(self):
        """
        Returns a dictionary with the n-digit code as the key and their corresponding
        ministry combinations as the values
        """
        ministry_combs_with_code = dict()
        all_ministry_combs = self.get_valid_ministry_combs()
        for i, m in enumerate(all_ministry_combs):
            ministry_combs_with_code[self.to_given_length(i)] = m
        return ministry_combs_with_code

    def to_given_length(self, val):
        """
        Returns string of a specified length (self.max_mininstry_code_len) for the value passed in
        """
        val = str(val)
        if len(val) > self.max_mininstry_code_len:
            raise ValueError(f'Unacceptable value: Value must have length of > 0 and <= {self.max_mininstry_code_len}')
        if len(val) == self.max_mininstry_code_len:
            return val
        return ('0' * (self.max_mininstry_code_len - len(val))) + val

m = MinistryCodeGen()
print(m.get_valid_ministry_combs())
