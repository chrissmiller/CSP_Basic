from CSP import ConstraintSatisfactionProblem

class MapSolverCSP(ConstraintSatisfactionProblem):

    def __init__(self, description, inference = False, mrv = False, random = False):
        self.territory_map = {}
        self.color_map = {}

        constraint_dict = {}
        base_domain = set()
        domain = {}

        pieces = description.splitlines()
        #num_connects = len(pieces) - 2
        territories = pieces[0].split()
        num_vars = len(territories)

        # Set up map from int to color
        i = 0
        colors = pieces[len(pieces) - 1].split()
        for color in colors:
            base_domain.add(i)
            self.color_map[i] = color
            self.color_map[color] = i
            i += 1

        # Set up map from int to territory name
        i = 0
        for territory in territories:
            domain[i] = base_domain
            self.territory_map[i] = territory
            self.territory_map[territory] = i
            i += 1


        # Set up constraint map
        constraints = pieces[1:len(pieces)-1]

        # Generates range of allowed values for adjacent territories
        valid = []
        for a in range(len(colors)):
            for b in range(len(colors)):
                if a != b:
                    valid.append((a,b))

        for constraint in constraints:
            names = constraint.split()
            if len(names) > 1:
                to_terr = self.territory_map[names[0]]
                for connected_name in names[1:]:
                    from_terr = self.territory_map[connected_name]
                    constraint_dict[(from_terr, to_terr)] = valid

        ConstraintSatisfactionProblem.__init__(self, num_vars, constraint_dict, domain, inference, mrv, random)

    # Converts result to string
    def resultToString(self, vars):
        res = ""
        for i in range(len(vars)):
            res += ("Territory " + self.territory_map[i] + " is colored " + self.color_map[vars[i]] + "\n")
        return res

def main():
    description = "WA NT Q NSW V SA T\nWA NT SA\nNT WA SA Q\nQ NT SA NSW\nNSW Q SA V\nV NSW SA\nRed Blue Green"
    mapCSP = MapSolverCSP(description, False, False, True)
    res = mapCSP.resultToString(mapCSP.backtrack())
    print(res)

if __name__ == "__main__":
    main()
