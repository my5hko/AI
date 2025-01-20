"""
Tic Tac Toe Player
"""

import math

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
    """
    actions = set([(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == EMPTY ])
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
