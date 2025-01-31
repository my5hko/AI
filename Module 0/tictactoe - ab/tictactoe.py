"""
Tic Tac Toe Player
"""

import math
import copy
from icecream import ic

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
#    return [[EMPTY, X, O], [O, X, EMPTY], [X, EMPTY, O]]

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
    print(f"result: {result}", f"action: {action}")
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
    if all(cell != EMPTY for row in board for cell in row) or winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    status = {None: 0, X: 1, O: -1}
    return status[winner(board)]

def maxValue(board, a, b):
    """
    Returns the value of the current board state using the max value method.

    Parameters:
    board (list): The current state of the board.
    a (float): Alpha value for pruning.
    b (float): Beta value for pruning.

    Returns:
    tuple: The maximum value of the current board state, updated alpha, and beta.
    """
    if terminal(board):
        return utility(board), a, b
    v = -math.inf

    for action in actions(board):
#        print(f"minValue for {action}: {minValue(result(board, action))}")
        minval, a, b = minValue(result(board, action), a, b)
        if minval > v:
            v = minval
        if v >= b:
             return v, a, b
        
        a = max(a, v)

    return v, a, b

def minValue(board, a, b):
    """
    Returns the minimum value of the current board state.

    Parameters:
    board (list): The current state of the board.
    a (float): Alpha value for pruning.
    b (float): Beta value for pruning.

    Returns:
    tuple: The minimum value of the current board state, updated alpha, and beta.
    """
    if terminal(board):
        return utility(board), a, b
    v = math.inf

    for action in actions(board):
#        print(f"maxValue for {action}: {maxValue(result(board, action))}")
        maxval, a, b = maxValue(result(board, action), a, b)
        if maxval < v:
            v = maxval
        if v <= a:
             return v, a, b

        b = min(b, v)

    return v, a, b



def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    Parameters:
    board (list of lists): The current state of the board.

    Returns:
    tuple: The coordinates of the best move.

    Explanation:
This code is a Python implementation of a minimax algorithm for game tree search. 
The algorithm is used to determine the best move for a player in a two-player game, such as chess or tic-tac-toe.

The actions(board) function returns a list of all possible moves for the current state of the game. T
he result(board, action) function returns the state of the game after the specified move has been made. 
The maxValue(state) function returns the maximum value of the game state, and the minValue(state) function returns the minimum value of the game state.

The code iterates over all possible moves using a for loop. 
For each move, it calculates the minimum value of the resulting game state using the minValue(result(board, action)) function. 
If this minimum value is less than the current best value (v), the current move is updated as the best move.

Finally, the code returns the best move found.

Note that the code also includes an alternative implementation using the max() function and a lambda expression. 
This alternative implementation is equivalent to the original code and is provided for comparison.

    """
    if terminal(board):
        return None
    if player(board) == X:
        v = -math.inf
        a = -math.inf
        b = math.inf
        move = None
        for action in actions(board):
            minval, a, b = minValue(result(board, action), a, b)
            if minval > v:
                v = minval
                move = action
                
        return move
    else:
        v = math.inf
        a = -math.inf
        b = math.inf
        move = None
        for action in actions(board):
            maxval, a, b = maxValue(result(board, action), a, b)
            if maxval < v:
                v = maxval
                move = action

        return move
