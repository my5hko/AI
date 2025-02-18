import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        Return all cells if all of them are mines
        """
        if self.count == len(self.cells):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        Return all cells if none of them are mines
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell) #1
        self.mark_safe(cell) #2
        cells= set()          #3 adding all neigbor cells to set, except the cell itself
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if 0<=i<self.height and 0<=j<self.width and (i,j) not in self.moves_made:
                    cells.add((i,j))
        new_knowledge = Sentence(cells, count) #3 creating new sentence object
        print('new knowledge raw:', new_knowledge)
        for mine in self.mines:
            new_knowledge.mark_mine(mine) #4 remove known mines from new sentence
        for safe in self.safes:
            new_knowledge.mark_safe(safe) #4 remove known safes from new sentence
#4 checking if all cells in new knowledge are mines or safes, if yes, adding them to known mines or safes, else ading new sentence to knowledge base
        if new_knowledge.known_mines() != None:
            self.mines.update(new_knowledge.known_mines())
        elif new_knowledge.known_safes() != None: 
            self.safes.update(new_knowledge.known_safes())
        else:
            if new_knowledge not in self.knowledge and len(new_knowledge.cells)>0:
                print('new knowledge clean:', new_knowledge)
                self.knowledge.append(new_knowledge) #3 adding new sentence to the knowledge base

        for sentence in self.knowledge:
            sentence.cells.difference_update(self.safes) #4 remove known safes from all sentences
            print('with mines:', sentence)
            for mine in self.mines:
                sentence.mark_mine(mine) #4 remove known mines from all sentences
            print('without mines:', sentence)
            
#5 if all cells in sentence are mines, adding them to known mines and removing sentence from knowledge base
            if sentence.known_mines() != None: 
                self.mines.update(sentence.known_mines())
                self.knowledge.remove(sentence)
#5 if all cells in sentence are safes, adding them to known safes and removing sentence from knowledge base
            elif sentence.known_safes() != None:
                self.safes.update(sentence.known_safes())
                self.knowledge.remove(sentence)
        print('safes:', self.safes)
        print('mines:', self.mines)
        for sentence1, sentence2 in itertools.combinations(self.knowledge, 2): #5 comparing all pairs of sentences
#5 if one sentence is subset of another, creating new sentence and adding it to knowledge base
            if sentence1.cells.issubset(sentence2.cells): 
                new_sentence = Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count)
                if new_sentence not in self.knowledge and len(new_sentence.cells)>0:
                    self.knowledge.append(new_sentence)
                    self.knowledge.remove(sentence2)
            if sentence2.cells.issubset(sentence1.cells):
                new_sentence = Sentence(sentence1.cells - sentence2.cells, sentence1.count - sentence2.count)
                if new_sentence not in self.knowledge and len(new_sentence.cells)>0:
                    self.knowledge.append(new_sentence)
                    self.knowledge.remove(sentence1)
        print('knowledge:', [str(knowledge) for knowledge in self.knowledge])


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return safe_moves.pop()
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    moves.add((i,j))
        if moves:
            return moves.pop()
        return None

