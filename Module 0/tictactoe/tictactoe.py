"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Args:
        board (list of lists): The current state of the board.

    Returns:
        str: The player who has the next turn.
    """
    count = sum(cell == EMPTY for row in board for cell in row) # using generator to count number of empty cells, if even player is X
    if count % 2 == 1 :
        player = X
    else:
        player = O
    return player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    This code defines a function called actions that takes a board as input and returns a set of all possible actions (i, j) available on the board. 
    Using enumerate ti get id and value for each element of the list
    The function uses a list comprehension to iterate over each row and column of the board and checks if the cell is empty. 
    If it is, the coordinates (i, j) are added to the actions set. Finally, the actions set is returned.
    """
    actions = set([(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == EMPTY ])
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    The code defines a function called result that takes two arguments: board and action. 
    The board argument is a 2D array representing the current state of the game, and the action argument is a tuple representing the coordinates of the move to be made.

    The function creates a copy of the board using the copy.deepcopy function to avoid modifying the original board. 
    It then checks if the cell at the specified coordinates is empty (EMPTY). 
    If it is, the function assigns the current player's symbol to that cell. 
    If the cell is not empty, the function raises a ValueError indicating that the action is not allowed for the current state.

    The function returns the resulting board after the move has been made.

    """
    result = copy.deepcopy(board)
    if result[action[0]][action[1]] == EMPTY:
        result[action[0]][action[1]] = player(board)
        return result
    else:
        raise ValueError(f"Action '{action}' is not allowed for current state. Cell is not empty")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    ------
    The code defines a function called winner that takes a single argument: board. 
    The board argument is a 2D array representing the current state of the game.

    The function iterates over the players (X and O) and checks for three-in-a-row wins in the rows, columns, and diagonals of the board. 
    If a player has three consecutive symbols in any of these directions, the function returns that player as the winner.

    If no player has three consecutive symbols in any direction, the function returns None to indicate that the game is still in progress or has ended in a draw.
    """
    for player in [X, O]:
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return player
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return player
    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not any(cell == EMPTY for row in board for cell in row) or winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    status = {None: 0, X: 1, O: -1}
    return status[winner(board)]

def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        v = -math.inf
        move = None
        for action in actions(board):
            if minValue(result(board, action)) > v:
                v = minValue(result(board, action))
                move = action
        return move
    else:
        v = math.inf
        move = None
        for action in actions(board):
            if maxValue(result(board, action)) < v:
                v = maxValue(result(board, action))
                move = action
        return move

#        move = max(actions(board), key=lambda action: minValue(result(board, action)))
#        return move
