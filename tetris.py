#!/usr/bin/env python
from tetrislib import *
import numpy as np
from pprint import pprint

# tetrislib defines the variable board and the functions drawboard() and getinput()
BLOCK_DIMENSION = 4

BLOCKS = [
    [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
    ]
]


class Block():
    def __init__(self, square_offsets):
        self.block = np.zeros((BLOCK_DIMENSION, BLOCK_DIMENSION))
        self.position = (0, 0)
        self.square_offsets = square_offsets
        for loc in square_offsets:
            self.block[loc[0], loc[1]] = 1

    def rotate(self):
        self.block = np.rot90(self.block)


class Board():
    def __init__(self, dimensions=None, board=None):
        if dimensions is None:
            dimensions = {"x": 10, "y": 10}
        if board is None:
            self.board = np.zeros(dimensions.values())
        else:
            self.board = board

    def add_block(self, block, location):
        start_row, start_col = location
        new_board = np.copy(self.board)
        # print(location)
        board_rows, board_cols = self.board.shape
        
        start_rows_at = -1 * min(0, location[0])
        end_rows_at = board_rows - (location[0])
        start_cols_at = -1 * min(0, location[1])
        end_cols_at = board_cols - (location[1])
        
        usable_block = block.block[start_rows_at:end_rows_at, start_cols_at:end_cols_at]
        usable_block_rows, usable_block_cols = usable_block.shape
        # print(end_rows_at)
        # print(end_cols_at)
        pprint(usable_block)

        update_start_row = max(0, start_row)
        update_start_col = max(0, start_col)
        new_board[update_start_row:update_start_row + usable_block_rows, update_start_col:update_start_col + usable_block_cols] += usable_block 
        return Board(board=new_board)


class Game():
    def __init__(self):
        self.board = Board()
        self.active_block = Block(BLOCKS[0])
        self.active_block_location = (0, 0)
        self.game_over = False

    def run(self):
        while not self.game_over:
            active_board = self.board.add_block(self.active_block, self.active_block_location)
            draw_board(active_board.board)
            next_move = getinput()
            if next_move == "up":
                self.active_block.rotate()
            else:
                self.active_block_location = move(self.active_block_location, next_move)


def move(location, move_type):
    if move_type == "left":
        return location[0], location[1] - 1
    elif move_type == "right":
        return location[0], location[1] + 1
    elif move_type == "down":
        return location[0] + 1, location[1]
    else:
        raise Exception("Bad move type")


def main():
    game = Game()
    game.run()
    # This example code draws a horizontal bar 4 squares long.
    # block = Block([(0, 0), (1, 0), (2, 0), (3, 0)])
    # pprint(block.block)
    # block.rotate()
    # pprint(block.block)
    # block.rotate()
    # pprint(block.block)
    # block.rotate()
    # pprint(block.block)

    # bb = Board()
    # bb = bb.add_block(block, (2, 0))

    # row = 2
    # board[row][5] = 1
    # board[row][6] = 1
    # board[row][7] = 1
    # board[row][8] = 1

    # draw_board(bb.board)

    # This code waits for input until the user hits a keystroke. getinput() returns one of "left", "up", "right",
    # "down".
    # print getinput()


if __name__ == '__main__':
    main()
