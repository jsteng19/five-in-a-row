import argparse
import numpy as np

self_turn_values = [[0, 0, 0], [0, 5, 10], [0, 60, 110], [0, 100, 1000], [0, 100000, 100000], [1000000, 1000000, 1000000]]
opponent_turn_values = [[0, 0, 0], [0, 4, 9], [0, 50, 100], [0, 100, 500], [0, 500, 10000], [1000000, 1000000, 1000000]]

def human(self_board, opponent_board, size):
    while True:
        print("Make a move")
        movestr = input()
        if len(movestr) in range(2, 4) and movestr[0].isalpha() and movestr[1:].isdigit():
            x_pos, y_pos = ord(movestr[0].lower()) - ord('a'), int(movestr[1:]) - 1
            if x_pos in range(size) and y_pos in range(size):
                if not (self_board[x_pos][y_pos] or opponent_board[x_pos][y_pos]):
                    break
                else:
                    print("That tile is occupied")
            else:
                print("Move was off the board")
        else:
            print("Invalid input format")

    print("Move played: " + str(movestr))
    self_board[x_pos][y_pos] = True

    return


def minimax(self_board, opponent_board, size, depth=2):

    x_pos, y_pos, value = minimax_helper(self_board, opponent_board, depth, True)
    print("Move played: " + chr(ord('a') + x_pos) + str(y_pos + 1))
    self_board[x_pos][y_pos] = True


def minimax_helper(self_board, opponent_board, depth, is_max, alpha=-float('inf'), beta=float('inf')):
    size = len(self_board)
    if depth == 0:
        return -1, -1, heuristic(self_board, opponent_board, is_max)

    value = -float('inf') if is_max else float('inf')
    x_pos, y_pos = -1, -1

    moves = []
    ranking_values = []
    for x in range(size):
        for y in range(size):
            if not(self_board[x][y] or opponent_board[x][y]) and adjacent(self_board, opponent_board, x, y):
                moves.append((x, y))
                self_board[x][y] = True
                ranking_values.append(heuristic(opponent_board, self_board, not is_max))
                self_board[x][y] = False
    ranked_moves = sorted(zip(ranking_values, moves))

    for _, (x, y) in ranked_moves:
        if not (self_board[x][y] or opponent_board[x][y]):
            self_board[x][y] = True
            _, _, v = minimax_helper(opponent_board, self_board, depth - 1, not is_max, alpha, beta)
            self_board[x][y] = False
            if is_max:
                if v > value:
                    value = v
                    x_pos = x
                    y_pos = y
                    alpha = max(alpha, value)

            else:
                if v < value:
                    value = v
                    x_pos = x
                    y_pos = y
                    beta = min(beta, value)

            if alpha >= beta:
                break

    return x_pos, y_pos, value


def adjacent(self_board, opponent_board, x, y):
    board = np.add(self_board, opponent_board)
    board = np.pad(board, 1, 'constant', constant_values=(0))


    return board[x][y] + board[x][y + 1] + board[x][y + 2] + board[x + 1][y] + board[x + 1][y + 2] + \
            board[x + 2][y] + board[x + 2][y + 1] + board[x + 2][y + 2]


def heuristic(self_board, opponent_board, is_max):
    if is_max:
        return single_player_value(self_board, opponent_board, self_turn_values)\
                - single_player_value(opponent_board, self_board, opponent_turn_values)
    else:
        return single_player_value(opponent_board, self_board, opponent_turn_values) \
               - single_player_value(self_board, opponent_board, self_turn_values)



def single_player_value(self_board, opponent_board, values):

    value = 0

    size = len(self_board)
    for self, opponent in (self_board, opponent_board), (np.transpose(self_board), np.transpose(opponent_board)):  # horizontal and vertical
        for x in range(size):
            count = 0
            prev_empty = False
            for y in range(size):
                if self[x][y]:
                    count += 1
                else:
                    if count >= 2:
                        value += values[count][prev_empty + (not opponent[x][y])]

                    count = 0
                    prev_empty = False
                    if not opponent[x][y]:
                        prev_empty = True

            if count >= 2:
                value += values[count][prev_empty]

    self_flip = np.flip(self_board, 1)
    opponent_flip = np.flip(opponent_board, 1)

    for self, opponent in (self_board, opponent_board), (np.flip(self_board, 0), np.flip(opponent_board, 0)), \
                          (np.delete(self_flip, 1, 0), np.delete(opponent_flip, 1, 0)), \
                          (np.delete(np.flip(self_flip, 0), 1, 0), np.delete(np.flip(opponent_flip, 0), 1, 0)):

        size = len(self)
        for starting_col in range(size - 4):  # 5-in-a-row impossible in the corners
            count = 0
            for row in range(size - starting_col):
                if self[starting_col + row][row]:
                    count += 1
                else:
                    if count >= 2:
                        value += values[count][prev_empty + (not opponent[starting_col + row][row])]

                    count = 0
                    prev_empty = not opponent[starting_col + row][row]

            if count >= 2:
                value += values[count][prev_empty]

    return value


def win(black_board, white_board):
    for board in black_board, white_board:

        transpose = np.transpose(board)
        flip = np.flip(board, 1)
        for b in board, transpose: # check across and down
            for col in b:
                count = 0
                for tile in col:
                    if tile:
                        count+=1
                    else:
                        count = 0
                    if count == 5:
                        return True

        for b in board, np.flip(board, 0), flip, np.flip(flip, 0):  #  covers right and left diagonals over both halves of the board
            for starting_col in range(len(board) - 4):  # 5-in-a-row impossible in the corner
                count = 0
                for row in range(len(board) - starting_col):
                    if b[starting_col + row][row]:
                        count += 1
                    else:
                        count = 0
                    if count == 5:
                        return True

    return False


def board_full(black_board, white_board):
    return np.prod(np.add(black_board, white_board))


def game_over(black_board, white_board):
    return win(black_board, white_board) or board_full(black_board, white_board)


def print_board(black_board, white_board):
    # print(black_board)
    # print(white_board)
    print("   " + " ".join([chr(l + ord("A")) for l in range(len(black_board))]))
    for row in range(len(black_board)):
        row_string = " " + str(row + 1) if row < 9 else str(row + 1)
        for col in range(len(black_board)):
            if black_board[col][row]:
                row_string += "|" + "B"
            elif white_board[col][row]:
                row_string += "|" + "W"
            else:
                row_string += "|" + " "
        row_string += "|"
        print(row_string)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", default=11)
    parser.add_argument("-l", action="store_true")
    args = parser.parse_args()
    board_size = int(args.n)
    human_first = not args.l

    black_board = np.zeros((board_size, board_size), dtype=np.bool)
    white_board = np.zeros((board_size, board_size), dtype=np.bool)

    if human_first:
        black_player = human
        white_player = minimax
    else:
        black_player = minimax
        white_player = human

    black_turn = True
    while not game_over(black_board, white_board):
        if black_turn:
            black_player(black_board, white_board, board_size)

        else:
            white_player(white_board, black_board, board_size)

        print_board(black_board, white_board)
        black_turn = not black_turn

    if win(black_board, white_board):
        if black_turn:
            print("White wins!")
        else:
            print("Black wins!")

    else:
        print("Tie")


main()
