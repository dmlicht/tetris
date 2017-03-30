#!/usr/bin/env python
from blocks import BLOCKS
from tetrislib import *
import numpy as np
import threading
import random

# tetrislib defines the variable board and the functions drawboard() and getinput()
BLOCK_DIMENSION = 4


class Block():
    """ Keeps track of offset positions, location and rotations of block """
    def __init__(self, square_offsets, position=(0, 0)):
        self.block = np.zeros((BLOCK_DIMENSION, BLOCK_DIMENSION))
        self.position = position
        self.square_offsets = square_offsets
        self.render_matrix()

    def rotate(self):
        self.square_offsets = [(col, BLOCK_DIMENSION - 1 - row) for row, col in self.square_offsets]

    def preview_rotate(self):
        rotated = [(col, BLOCK_DIMENSION - 1 - row) for row, col in self.square_offsets]
        for offset in rotated:
            yield (self.position[0] + offset[0], self.position[1] + offset[1])

    def get_absolute_locations(self):
        for offset in self.square_offsets:
            yield (self.position[0] + offset[0], self.position[1] + offset[1])

    def preview_move(self, move_offset):
        for offset in self.square_offsets:
            yield (self.position[0] + offset[0] + move_offset[0], self.position[1] + offset[1] + move_offset[1])

    def render_matrix(self):
        self.block = np.zeros((BLOCK_DIMENSION, BLOCK_DIMENSION))
        for loc in self.square_offsets:
            self.block[loc[0], loc[1]] = 1
        return self.block


class Board():
    def __init__(self, dimensions=None, board=None):
        if dimensions is None:
            dimensions = {"x": 10, "y": 10}
        if board is None:
            self._board = np.zeros(dimensions.values())
        else:
            self._board = board

    def anchor(self, block):
        self._board = self._add_block_to_board(block)

    def preview_with_block(self, block):
        new_board = self._add_block_to_board(block)
        return Board(board=new_board)

    def _add_block_to_board(self, block):
        new_board = np.copy(self._board)
        for location in block.get_absolute_locations():
            new_board[location[0], location[1]] += 1
        return new_board

    def can_place_block(self, block_locations):
        for location in block_locations:
            for dim in range(2):
                if location[dim] >= self._board.shape[dim] or location[dim] < 0:
                    return False
            if self._board[location[0], location[1]] > 0:
                return False
        return True

    def can_move_down(self, block):
        return self.can_move_offset(block, (1, 0))

    def can_move_offset(self, block, offset):
        for location in block.get_absolute_locations():
            offset_location = location[0] + offset[0], location[1] + offset[1]
            for dim in range(2):
                if offset_location[dim] >= self._board.shape[dim] or offset_location < 0:
                    return False
            if self._board[offset_location[0], offset_location[1]] > 0:
                return False
        return True

    def clear(self):
        """ Clears full bottom rows and returns amount of rows cleared """
        rows_cleared = 0
        ii = self._board.shape[0] - 1
        while ii >= 0:
            row_full = all(self._board[ii, :])
            if row_full:
                rows_cleared += 1
                ii -= 1
            else:
                break

        self.remove_bottom_n_rows(rows_cleared)
        return rows_cleared

    def remove_bottom_n_rows(self, n):
        if n == 0:
            return
        self._board[-1 * n:, :] = 0
        self._board = np.roll(self._board, n, axis=0)


def next_block():
    rand = random.randint(0, len(BLOCKS) - 1)
    return Block(BLOCKS[rand])


MOVES = {
    'right': (0, 1),
    'left': (0, -1),
    'down': (1, 0)
}


class Game():
    def __init__(self):
        self.board = Board()
        self.active_block = next_block()
        self.game_over = False
        self.points = 0

    def run(self):
        # t = threading.Timer(3.0, self.handle_down)
        # t.start()
        while not self.game_over:
            active_board = self.board.preview_with_block(self.active_block)
            print("score:", self.points)
            draw_board(active_board._board)
            next_move = getinput()
            if next_move == "up":
                if self.board.can_place_block(self.active_block.preview_rotate()):
                    self.active_block.rotate()
            elif next_move == "left":
                if self.board.can_place_block(self.active_block.preview_move(MOVES['left'])):
                    self.active_block.position = move(self.active_block.position, next_move)
            elif next_move == "right":
                if self.board.can_place_block(self.active_block.preview_move(MOVES['right'])):
                    self.active_block.position = move(self.active_block.position, next_move)
            elif next_move == "down":
                if self.board.can_move_down(self.active_block):
                    self.active_block.position = move(self.active_block.position, "down")
                else:
                    self.board.anchor(self.active_block)
                    self.points += self.board.clear()
                    self.active_block = next_block()
                    if not self.board.can_place_block(self.active_block.get_absolute_locations()):
                        self.game_over = True
        print("Game over, you got " + str(self.points) + " points.")

    def handle_down(self):
        if self.board.can_move_down(self.active_block):
            self.active_block.position = move(self.active_block.position, "down")
        else:
            self.board.anchor(self.active_block)
            self.points += self.board.clear()
            self.active_block = next_block()
            if not self.board.can_place_block(self.active_block.get_absolute_locations()):
                self.game_over = True


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


if __name__ == '__main__':
    main()
