import heapq
import random

class ConstraintSatisfactionProblem:
    def __init__(self, num_vars, constraint_dict, domain, inference = False, mrv = False, random = False):
        self.constraint_dict = constraint_dict
        self.num_vars = num_vars
        self.domain = domain
        self.num_i_calls = 0
        self.num_b_calls = 0
        self.MRVqueue = []
        self.use_inference = inference
        self.use_mrv = mrv
        self.randomsel = random

        for i in range(self.num_vars):
            heapq.heappush(self.MRVqueue, (len(self.domain[i]), i)) #priority queue

    # Checks if the assignment is a solution
    def validate(self, vars):
        for key in self.constraint_dict:
            valid_vals = self.constraint_dict[key]
            if (vars[key[0]], vars[key[1]]) not in valid_vals:
                return False
        return True

    # Initializes backtrack search with no var assignments
    def backtrack(self):
        vars = [None]*self.num_vars
        return self.backtrack_search(vars)

    # Recursive search
    def backtrack_search(self, vars):
        self.num_b_calls += 1
        if None not in vars:
            if self.validate(vars):
                return vars
            else:
                return False

        var = self.get_unassigned(vars)
        val_domain = set(self.get_domain_vals(var, vars))

        while val_domain:
            val = val_domain.pop()
            oldvars = vars.copy()

            for i in range(self.num_vars):
                ival = vars[i]
                if ival != None:
                    valid = False
                    if (var, i) in self.constraint_dict:
                        valid = (val, ival) in self.constraint_dict[(var, i)]
                    else: # No arc between the two variables
                        valid = True
                else:
                    valid = True

                if not valid:
                    break

            # Val is consistent with vars & constraint dict
            vars[var] = val
            if self.use_inference:
                if self.inference(vars, var, val):
                    vars = self.backtrack_search(vars)
                    if vars:
                        return vars
            else:
                vars = self.backtrack_search(vars)
                if vars:
                    return vars
            vars = oldvars
        heapq.heappush(self.MRVqueue, (len(self.domain[var]), var))

        return False

    # Use AC-3 Algorithm to enforce arc consistency
    def inference(self, vars, var, val):
        to_remove = set()
        self.num_i_calls += 1
        arcs = set(self.constraint_dict.keys())
        for arc in arcs:
            if arc[1] != var:
                to_remove.add(arc)

        arcs -= to_remove

        to_remove.clear()

        while arcs:
            arc = arcs.pop()
            possibles = self.constraint_dict[arc]
            deletions = False
            for a_val in self.domain[arc[0]]:
                valid = False
                for possible in possibles:
                    if possible[0] == a_val:
                        valid = True
                if not valid:
                    deletions = True
                    to_remove.add(a_val)
            self.domain[arc[0]] -= to_remove
            to_remove.clear()

            # Inference failed
            if len(self.domain[arc[0]]) < 1:
                return False

            # add arcs to A to the set for updates
            if deletions:
                for point_arc in self.constraint_dict:
                    if point_arc[1] == arc[0]:
                        arcs.add(point_arc)
        return True


    # Gets an unassigned variable from vars
    def get_unassigned(self, vars):
        if self.use_mrv:
            var = heapq.heappop(self.MRVqueue)
            return var[1]
        elif self.randomsel:
            var_list = list(range(self.num_vars))
            random.shuffle(var_list)
            for i in var_list:
                if vars[i] == None:
                    return i
        else:
            for i in range(self.num_vars):
                if vars[i] == None:
                    return i

    # Gets domain values for the given var and assignment
    def get_domain_vals(self, var, vars):
        return self.domain[var]
