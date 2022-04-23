"""
Tic Tac Toe Player
"""
import copy
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
    """
    # initialize x_count and o_count
    x_count = 0
    o_count = 0

    # count number of x and o in the board
    for rows in board:
        x_count += rows.count(X)
        o_count += rows.count(O)

    # assuming the initial move is always made by x player:
    # if number of x and o are the same, x is the next player
    if x_count == o_count or x_count < o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action:
        i = action[0]
        j = action[1]

        # deep copy of the original board
        new_board = copy.deepcopy(board)

        # if action is empty raise an error
        if board[i][j] != EMPTY:
            raise Exception("not a valid action")
        # else update the baord with the players action
        else:
            new_board[i][j] = player(board)

        return new_board

    else:
        return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # initial counts for diagonals
    x_diag_right = 0
    o_diag_right = 0
    x_diag_left = 0
    o_diag_left = 0

    # check for winner
    for i in range(3):

        # reset counter lists for horizontal and vertical
        # but keep track of diagonal counts
        x_list = [x_diag_right, 0, 0, x_diag_left]
        o_list = [o_diag_right, 0, 0, o_diag_left]

        for j in range(3):

            # right diagonal
            if i == j:
                if board[i][j] == X:
                    x_list[0] += 1
                elif board[i][j] == O:
                    o_list[0] += 1

            # left diagonal
            if i+j == 2:
                if board[i][j] == X:
                    x_list[3] += 1
                elif board[i][j] == O:
                    o_list[3] += 1

            # vertical
            if board[j][i] == X:
                x_list[1] += 1
            elif board[j][i] == O:
                o_list[1] += 1

            # horizontal
            if board[i][j] == X:
                x_list[2] += 1
            elif board[i][j] == O:
                o_list[2] += 1

        # update diagonals
        x_diag_right = x_list[0]
        o_diag_right = o_list[0]
        x_diag_left = x_list[3]
        o_diag_left = o_list[3]

        # check if any of the counts is 3
        if 3 in x_list:
            return X
        elif 3 in o_list:
            return O
        else:
            continue

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if there's a winner, game over
    if winner(board):
        return True

    else:
        # if no winner check if board is filled
        for rows in board:
            if EMPTY in rows:
                # no winner yet, but is not filled
                return False

    # no winner, but board is filled so game over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
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
    # terminate
    if terminal(board):
        return None
    elif len(actions(board)) == 9:
        return(1, 1)
    # else:
    # maximizing player
    if player(board) == X:
        best_score = -100
        best_move = None
        moves = actions(board)

        for move in moves:
            temp_board = result(copy.deepcopy(board), move)
            min_value_result = min_value(temp_board)
            if min_value_result > best_score:
                best_score = min_value_result
                best_move = move

    # minimizing player
    else:
        best_score = 100
        best_move = None
        moves = actions(board)

        for move in moves:
            temp_board = result(copy.deepcopy(board), move)
            max_value_result = max_value(temp_board)
            if max_value_result < best_score:
                best_score = max_value_result
                best_move = move

    return best_move


def max_value(board):
    if terminal(board):
        return utility(board)
    best_score = -100
    for action in actions(board):
        best_score = max(best_score, min_value(result(board, action)))
    return best_score


def min_value(board):
    if terminal(board):
        return utility(board)
    best_score = 100
    for action in actions(board):
        best_score = min(best_score, max_value(result(board, action)))
    return best_score
