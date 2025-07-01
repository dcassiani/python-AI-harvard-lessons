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
    """
    #raise NotImplementedError
    xMoves = 0
    yMoves = 0

    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == X:
                xMoves += 1
            elif board[r][c] == O:
                yMoves += 1

    if xMoves > yMoves:
        return O
    else:
        return X
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #raise NotImplementedError
    possible_actions = set()

    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY:
                possible_actions.add((r, c))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
#    raise NotImplementedError
    if action not in actions(board):
        raise Exception("Invalid move")

    new_board = copy.deepcopy(board) # use copy import to preserve original instance of board
    r, c = action # actual new move to be added to the board

    new_board[r][c] = player(board)
    return new_board

def checkIfPlayerWon(board, player):
    """
    Helper function to check if a player has won the game.
    """
    for row in range(len(board)):
        if board[row][0] == player \
            and board[row][1] == player \
            and board[row][2] == player:
                return True

    for col in range(len(board[0])):
        if board[0][col] == player \
            and board[1][col] == player \
            and board[2][col] == player:
                return True

    playerPiecesCountInSameDiagonal = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if row == col and board[row][col] == player:
                playerPiecesCountInSameDiagonal += 1
    if playerPiecesCountInSameDiagonal == 3:
        return True 
    
    playerPiecesCountInSameDiagonal = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if (len(board) - row -1) == col and board[row][col] == player:
                playerPiecesCountInSameDiagonal += 1
    if playerPiecesCountInSameDiagonal == 3:
        return True 

    return False



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #raise NotImplementedError
    if checkIfPlayerWon(board, X):
        return X
    elif checkIfPlayerWon(board, O):
        return O
    else:
        return None


    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #raise NotImplementedError
    if winner(board) == X:
        return True
    if winner(board) == O:
        return True
    
    for row in range(len(board)):   
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                return False
    
    return True # TIE


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #raise NotImplementedError
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #raise NotImplementedError
    if terminal(board):
        return None
    
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
    if terminal(board):
        return None
    
    #max player (X)
    elif player(board) == X:
        possiblePlays = []
        for action in actions(board):
            # add to the list the min  score for the action
            possiblePlays.append([minValue(result(board, action)), action])
            # order the list by the max score to have the best move on top
        return sorted(possiblePlays, key=lambda x: x[0], reverse=True)[0][1]
    
    #min player (O)
    else:
        possiblePlays = []
        for action in actions(board):
            # add to the list the max score for the action
            possiblePlays.append([maxValue(result(board, action)), action])
            # order the list - max score for best move is already on top
        return sorted(possiblePlays, key=lambda x: x[0])[0][1]
    
