import sys
from icecream import ic

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        # debug prints
        ic(self.crossword.overlaps)
        for var in self.crossword.variables:
            ic(var, self.crossword.neighbors(var)) 

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        ic(self.domains)
        
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            # Remove values from `self.domains[var]` that are not of the same
            # length as the variable's length.
            self.domains[var] = { # using set comprehension
                word for word in self.domains[var]
                if len(word) == var.length
            }
            # for word in list(self.domains[var]):  # using set.remove() method
            #     if len(word) != var.length:
            #         self.domains[var].remove(word)
        ic(self.domains)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        if self.crossword.overlaps[x,y] :
            i, j = self.crossword.overlaps[x,y]
            # Remove values from `self.domains[x]` that are not consistent with
            # the corresponding value in `self.domains[y]`.
            for word_x in list(self.domains[x]):
                if not any(word_x[i] == word_y[j] for word_y in self.domains[y]):
                    self.domains[x].remove(word_x)
                    revised = True
        return revised

        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = [(x,y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]
        queue = arcs.copy()
        while queue:
            ic (queue)
            x, y = queue.pop(0)
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z,x)) if (z,x) not in queue else None
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if all words are unique
        if len(assignment) != len(set(assignment.values())):
            return False
        # Check if all words are of correct length
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
            # Check if words are consistent with each other
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if word[i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Count the number of domain values for each var that is ruled out 
        words = []
        for word in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    for word_neighbor in self.domains[neighbor]:
                        if word[i] != word_neighbor[j]:
                            count += 1
            words.append((count, word))
        # Sort the values by the number of ruled out values
        sorted_words = sorted(words, key=lambda x: x[0])
        # Return only the words, not the counts
        return [word for count, word in sorted_words]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Select the unassigned variable with the min number of values in its domain
        unassigned_vars = [(var, len(self.domains[var])) for var in self.crossword.variables if var not in assignment]
        if not unassigned_vars:
            return None
        # Sort by number of values in domain and degree (ascending by number of values, descending by degree)
        unassigned_vars.sort(key=lambda x: (x[1], -len(self.crossword.neighbors(x[0]))))
        # Return the variable with the minimum number of values in its domain
        return unassigned_vars[0][0] # first value of the first tuple
        # return min(unassigned_vars, key=lambda x: (x[1], -len(self.crossword.neighbors(x[0]))))[0] # single line version

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If assignment complete return it
        if self.assignment_complete(assignment):
            return assignment
        # Select unassigned variable
        var = self.select_unassigned_variable(assignment)
        # Iterate over ordered domain values
        for value in self.order_domain_values(var, assignment):
            # Add value to assignment
            assignment[var] = value
            # Check if assignment is consistent
            if self.consistent(assignment):
                # Recur to assign remaining variables
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            # Remove value from assignment
            del assignment[var]
        # If no assignment is possible, return None
        return None
        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
