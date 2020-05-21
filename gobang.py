import argparse
import operator

import random


def human(black_board, white_board):
    while True:
        print("Make a move (<letter><number>)")
        movestr = input()
        if len(movestr) == 2 and movestr[0].isalpha() and movestr[1].isdigit():
            x_pos, y_pos = ord(movestr[0]) - ord('A'), int(movestr[1])
            if x_pos < len(black_board) and y_pos <= len(black_board):
                if not black_board[x_pos][y_pos] or white_board[x_pos][y_pos]:
                    break
                else:
                    print("That tile is occupied")
            else:
                print("Move was off the board")
        else:
            print("Invalid input format")

    print("Move played: " + str(movestr))
    return x_pos, y_pos

def ai(black_board, white_board):
    x, y = random.randint(0, len(black_board)), random.randint(0, len(black_board))
    while black_board[x][x] or white_board[x][x]:
        x, y = random.randint(0, len(black_board)), random.randint(0, len(black_board))

    print("Move played: " + chr(ord('A') + x) + str(y))
    return x, y

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", default=11)
    parser.add_argument("-l", action="store_true")
    args = parser.parse_args()
    board_size = args.n
    human_first = not args.l


    black_board = [[False for i in range(board_size)] for i in range(board_size)]
    white_board = [[False for i in range(board_size)] for i in range(board_size)]

    if human_first:
        black_player = human
        white_player = ai
    else:
        black_player = ai
        white_player = human

    black_turn = True
    while not game_over(black_board, white_board):
        if black_turn:
            move = black_player(black_board, white_board)
            black_board[move[0]][move[1]] = True

        else:
            move = white_player(black_board, white_board)
            white_board[move[0]][move[1]] = True

        black_turn = not black_turn


    if(win(black_board, white_board)):
        if black_turn:
            print("White wins!")
        else:
            print("Black wins!")

    else:
        print("Tie")


main()