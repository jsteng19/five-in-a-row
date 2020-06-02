import argparse

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
    # x_pos, y_pos = random.randint(0, len(self_board) - 1), random.randint(0, len(self_board) - 1)
    # while self_board[x_pos][y_pos] or opponent_board[x_pos][y_pos]:
    #     x_pos, y_pos = random.randint(0, len(self_board) - 1), random.randint(0, len(self_board) - 1)

    value = -float('inf')
    x_pos, y_pos = -1, -1
    for x in range(len(self_board)):
        for y in range(len(self_board)):
            if not (self_board[x][y] or opponent_board[x][y]):
                self_board[x][y] = True
                v = heuristic(self_board, opponent_board)
                self_board[x][y] = False
                if v > value:
                    value = v
                    x_pos = x
                    y_pos = y


    print("Move played: " + chr(ord('A') + x_pos) + str(y_pos + 1) + "value = " + str(value))
    self_board[x_pos][y_pos] = True
    return


def heuristic(self_board, opponent_board): # doesn't account for blanks between consecutive tiles

    value = 0
    self_transpose = list(zip(*self_board))
    opponent_transpose = list(zip(*opponent_board))
    self_flip = [list(reversed(column)) for column in self_board]
    opponent_flip = [list(reversed(column)) for column in opponent_board]

    for self, opponent in (self_board, opponent_board), (self_transpose, opponent_transpose):  # horizontal and vertical
        for x in range(len(self)):
            count = 0
            prev_empty = False
            post_empty = False
            for y in range(len(self)):
                if self[x][y]:
                    count += 1
                else:
                    if count >= 2:
                        if not opponent[x][y]:
                            post_empty = True
                        empty = prev_empty + post_empty
                        value += self_values(count, empty)

                    count = 0
                    post_empty = False
                    prev_empty = False
                    if not opponent[x][y]:
                        prev_empty = True

            if count >= 2:
                value += self_values(count, prev_empty)

    for self, opponent in (self_board, opponent_board), (list(reversed(self_board)), list(reversed(opponent_board))),\
            (self_flip[1:], opponent_flip[1:]), (list(reversed(self_flip))[1:], list(reversed(opponent_flip))[1:]):
        # print_board(self, opponent)
        for starting_col in range(len(self) - 4):  # 5-in-a-row impossible in the corners
            count = 0
            prev_empty = False
            post_empty = False
            for row in range(len(self) - starting_col):
                if self[starting_col + row][row]:
                    count += 1
                else:

                    if not opponent[starting_col + row][row]:
                        post_empty = True

                    if count >= 2:
                        empty = prev_empty + post_empty
                        value += self_values(count, empty)

                    count = 0
                    prev_empty = False
                    if post_empty:
                        prev_empty = True
                    post_empty = False

            if count >= 2:
                value += self_values(count, prev_empty)

    return value


def self_values(length, empty):
    print("length:" + str(length) + ", empty: " + str(empty))
    if length == 5:
        return 100000 # 100,000 - win

    if empty == 0:
        return 0

    if length == 4:
        if empty == 2:
            return 1000 # guaranteed win if no opponent win
        if empty == 1:
            return 500

    if length == 3:
        if empty == 2:
            return 500 # guaranteed win if no opponent counter or edge
        if empty == 1:
            return 100

    if length == 2:
        if empty == 2:
            return 100
        if empty == 1:
            return 50



def opponent_values(length, empty):

    if length == 4:
        if empty > 0:
            return -10000  # guaranteed loss if no current win

    if length == 3:
        if empty == 2:
            return -5000  # guaranteed loss if no win within 1 turn
        if empty == 1:
            return -100

    if length == 2:
        if empty == 2:
            return -100  # guaranteed win if no opponent win
        if empty == 1:
            return -50


def win(black_board, white_board):
    for board in black_board, white_board:

        transpose = list(zip(*board))
        flip = [list(reversed(column)) for column in board]
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

        for b in board, list(reversed(board)), flip, list(reversed(flip)): # covers right and left diagonals over the both halves of the board
            for starting_col in range(len(board) - 4): # 5-in-a-row impossible in the corner
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
    for row in range(len(black_board[0])):
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

    while (True):
        black_player(black_board, white_board)
        print_board(black_board, white_board)
        print("value: " + str(heuristic(black_board, white_board)))

main()
