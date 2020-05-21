import argparse
import pprint

import random


def human(self_board, opponent_board):
    while True:
        print("Make a move")
        movestr = input()
        if len(movestr) < 4 and movestr[0].isalpha() and movestr[1:].isdigit():
            x_pos, y_pos = ord(movestr[0].lower()) - ord('a'), int(movestr[1:]) - 1
            if x_pos in range(len(self_board)) and y_pos in range(len(self_board)):
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


def ai(self_board, opponent_board):
    x, y = random.randint(0, len(self_board) - 1), random.randint(0, len(self_board) - 1)
    while self_board[x][y] or opponent_board[x][y]:
        x, y = random.randint(0, len(self_board) - 1), random.randint(0, len(self_board) - 1)

    print("Move played: " + chr(ord('A') + x) + str(y + 1))
    self_board[x][y] = True
    return


def win(black_board, white_board):
    for board in black_board, white_board:
        transpose = list(zip(*board))
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

        for b in board, list(reversed(board)), transpose, list(reversed(transpose)): # covers right and left diagonals over the both halves of the board
            for starting_col in range(len(board)):
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
    return all([all([any(pair) for pair in zip(column[0], column[1])]) for column in zip(black_board, white_board)])


def game_over(black_board, white_board):
    return win(black_board, white_board) or board_full(black_board, white_board)


def print_board(black_board, white_board):
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

    black_board = [l[:] for l in [[False]*board_size]*board_size]
    white_board = [l[:] for l in [[False]*board_size]*board_size]

    if human_first:
        black_player = human
        white_player = ai
    else:
        black_player = ai
        white_player = human

    black_turn = True
    while not game_over(black_board, white_board):
        if black_turn:
            black_player(black_board, white_board)

        else:
            white_player(white_board, black_board)

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
