import random

class MinConflicts:
    def __init__(self, num_vars, constraint_dict, domain):
        self.constraint_dict = constraint_dict
        self.num_vars = num_vars
        self.domain = domain
        self.num_calls = 0

    # Validates that
    def validate(self, vars):
        for key in self.constraint_dict:
            valid_vals = self.constraint_dict[key]
            if (vars[key[0]], vars[key[1]]) not in valid_vals:
                return False
        return True

    # Implements the min-conflicts algorithm
    def min_conflicts(self, max_steps):
        vars = self.assign()

        for i in range(max_steps):
            if self.validate(vars):
                self.num_calls = i + 1
                return vars

            self.set_conflict_table(vars)

            var = self.get_conflicted()
            vars[var] = self.min_conflict_val(var, vars)


        return False

    # Assigns a random value to each variable from its domain
    def assign(self):
        vars = [None]*self.num_vars
        for i in range(self.num_vars):
            vars[i] =  random.choice(tuple(self.domain[i]))

        return vars


    # Gets a conflicted variable
    def get_conflicted(self):
        conflicted = []

        for i in range(self.num_vars):
            if self.conflict_table[i] > 0:
                conflicted.append(i)

        return random.choice(conflicted)

    # Returns the value in the domain of var which minimizes conflicts
    def min_conflict_val(self, var, vars):
        min_conflicts = float("inf")
        min_val = None

        for val in self.domain[var]:
            num_conflicts = self.get_num_conflicts(vars, var, val)
            if num_conflicts < min_conflicts:
                min_conflicts = num_conflicts
                min_val = val
        return min_val

    # Sets a table with number of conflicts for each variable
    def set_conflict_table(self, vars):
        possibles = []
        self.conflict_table = [0]*self.num_vars
        for var in range(self.num_vars - 1):
            val = vars[var]
            for i in range(var + 1, self.num_vars):
                conflict = True
                if i == var or (var, i) not in self.constraint_dict:
                    continue
                possibles = self.constraint_dict[(var, i)]
                val2 = vars[i]

                if (val, val2) in possibles:
                    conflict = False
                if conflict:
                    self.conflict_table[var] += 1
                    self.conflict_table[i] += 1

    # Returns the number of other variables conflicting with the given var
    def get_num_conflicts(self, vars, var, val):
        possibles = []
        conflict_count = 0
        for i in range(self.num_vars):
            conflict = True
            if i == var or (var, i) not in self.constraint_dict:
                continue

            possibles = self.constraint_dict[(var, i)]

            if (val, vars[i]) in possibles:
                conflict = False

            if conflict:
                conflict_count += 1
        return conflict_count
