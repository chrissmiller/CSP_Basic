from CSP import ConstraintSatisfactionProblem
from itertools import product
from ast import literal_eval
import timeit
from min_conflicts import MinConflicts

class CircuitMin(MinConflicts):

    # Width by Height form
    def __init__(self, description):
        pieces = description.splitlines()
        pieces[0] = pieces[0].replace(" ", "")
        board = pieces[0].split(":")
        componentDesc = pieces[1:]
        self.name_map = {}

        # Parses board dimensions
        self.dim = literal_eval(board[1])
        n = self.dim[0]
        m = self.dim[1]

        domain = {}
        constraint_dict = {}
        num_vars = len(componentDesc)

        # Parses component sizes
        components = num_vars*[None]
        for i in range(num_vars):
            componentDesc[i] = componentDesc[i].replace(" ", "")
            comp = componentDesc[i].split(":")
            components[i] = literal_eval(comp[1])
            self.name_map[i] = comp[0]

        self.components = components
        num_vars = len(components)

        # Generates all domain values for each component
        for i in range(len(components)):
            item = components[i]
            y_dom = list(range(m + 1 - item[1])) # All possible y coordinates
            x_dom = list(range(n + 1 - item[0])) # All possible x coordinates
            domain[i] = set(product(x_dom, y_dom))


        for i in range(num_vars - 1):
            for j in range(i + 1, num_vars):
                for ipos in domain[i]:
                    for jpos in domain[j]:
                        if not self.overlap(components[i], components[j], ipos, jpos):
                            if (i,j) not in constraint_dict:
                                constraint_dict[(i,j)] = []
                            if (j,i) not in constraint_dict:
                                constraint_dict[(j,i)] = []

                            constraint_dict[(i, j)].append((ipos,jpos))
                            constraint_dict[(j, i)].append((jpos,ipos))
                if (i,j) not in constraint_dict:
                    constraint_dict[(i,j)] = []
                    constraint_dict[(j,i)] = []


    #    print("beep")

        MinConflicts.__init__(self, num_vars, constraint_dict, domain)

    # Converts variable positions and height and widths
    # to an ASCII circuitboard
    def resultToString(self, vars):
        width = self.dim[0]
        height = self.dim[1]

        index  = []

        for i in range(width):
            index.append([])
            index[i] = ["*"]*height

        for i in range(self.num_vars):
            symbol = self.name_map[i]
            widthi = self.components[i][0]
            heighti = self.components[i][1]
            x = vars[i][0]
            y = vars[i][1]

            for col in range(x, x+widthi):
                for row in range(y, y+heighti):
                    index[col][row] = symbol
        rep = ""
        for row in range(height-1, -1, -1):
            for col in range(width):
                rep += index[col][row]
            rep += "\n"

        return rep

    # Algorithm for checking rectangle overlap
    # derived from algorithm found at:
    # https://www.geeksforgeeks.org/find-two-rectangles-overlap/

    def overlap(self, rect1, rect2, pos1, pos2):
        left1 = (pos1[0], pos1[1] + rect1[1] - 1)
        right1 = (pos1[0] + rect1[0] - 1, pos1[1])

        left2 = (pos2[0], pos2[1] + rect2[1] - 1)
        right2 = (pos2[0] + rect2[0] - 1, pos2[1])

        return not (left1[1] < right2[1] or left2[1] < right1[1] or left1[0] > right2[0] or left2[0] > right1[0])

def main():
    tester = CircuitMin("Board: (17, 3)\na: (10, 2)\nb: (5, 2)\nc: (2, 3)\ne: (7, 1)")
    #tester = CircuitCSP("Board: (10, 3)\na: (3, 2)\nb: (5, 2)\ne: (7, 1)", False, True)
    #tester = CircuitCSP("Board: (4, 3)\na: (2, 2)\nb: (2, 3)\nc: (2, 1)")

    result = tester.min_conflicts(30000)
    if result:
        print(tester.resultToString(result))
    else:
        print("No valid configuration found.")
    print("Used " + str(tester.num_calls) + " steps.")
    #print("Result found: " + str(result))



if __name__ == "__main__":
    main()
